# from django.core.management.base import BaseCommand
# from django.core.management import call_command
# from pathlib import Path
# import shutil

# class Command(BaseCommand):
#     help = 'Restore the latest backup migration for a given app'

#     def add_arguments(self, parser):
#         parser.add_argument('app_name', type=str, help='App name to restore migration')

#     def handle(self, *args, **kwargs):
#         app_name = kwargs['app_name']
#         migration_path = Path(f"{app_name}/migrations")
#         backup_path = migration_path / "backups"

#         if not backup_path.exists():
#             self.stdout.write(self.style.ERROR(f"No backup folder found for app: {app_name}"))
#             return

#         backup_files = sorted(backup_path.glob("*.py"))
#         if not backup_files:
#             self.stdout.write(self.style.WARNING("No backup files found."))
#             return

#         latest_backup = backup_files[-1]
#         destination = migration_path / latest_backup.name

#         # Step 1: Copy back to migrations
#         shutil.copy(latest_backup, destination)
#         self.stdout.write(self.style.SUCCESS(f"Restored: {latest_backup.name} to {destination}"))

#         # Step 2: Run migrate
#         call_command("migrate", app_name)
#         self.stdout.write(self.style.SUCCESS("Migration applied successfully."))


# restored migration file
# ----------------------------------------------------------------------------------
from django.core.management.base import BaseCommand
from django.core.management import call_command
from pathlib import Path
import shutil
from django.db.migrations.loader import MigrationLoader
from django.db import connection

class Command(BaseCommand):
    help = 'Restore last migration file from backup and apply migration (even if no migration exists)'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='App name to restore migration')

    def handle(self, *args, **kwargs):
        app_name = kwargs['app_name']

        try:
            loader = MigrationLoader(connection, ignore_no_migrations=True)
            graph = loader.graph

            leaf_nodes = graph.leaf_nodes(app_name)
            rollback_apps = []

            if leaf_nodes:
                target_node = leaf_nodes[-1]
                rollback_plan = graph.forwards_plan(target_node)

                for app_label, _ in rollback_plan:
                    if app_label not in rollback_apps:
                        rollback_apps.append(app_label)

                rollback_apps = rollback_apps[::-1]

            # Ensure the requested app is included
            if app_name not in rollback_apps:
                rollback_apps.insert(0, app_name)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[{app_name}] Failed to load migration graph: {e}"))
            rollback_apps = [app_name]  # Fallback to only the target app

        for app in rollback_apps:
            try:
                migration_path = Path(f"{app}/migrations")
                backup_path = migration_path / "backups"

                if not backup_path.exists():
                    self.stdout.write(self.style.WARNING(f"[{app}] No backup folder found. Skipping."))
                    continue

                backup_files = sorted(backup_path.glob("*.py"))
                if not backup_files:
                    self.stdout.write(self.style.WARNING(f"[{app}] No backup files found. Skipping."))
                    continue

                latest_backup = backup_files[-1]
                destination = migration_path / latest_backup.name

                # Step 1: Restore backup file
                shutil.copy(latest_backup, destination)
                self.stdout.write(self.style.SUCCESS(f"[{app}] Restored: {latest_backup.name}"))

                # Step 2: Apply migration
                try:
                    call_command("makemigrations", app)
                except Exception as mk_err:
                    self.stdout.write(self.style.WARNING(f"[{app}] makemigrations skipped or failed: {mk_err}"))

                try:
                    call_command("migrate", app)
                    self.stdout.write(self.style.SUCCESS(f"[{app}] Migration applied successfully."))
                except Exception as migrate_err:
                    self.stdout.write(self.style.ERROR(f"[{app}] Migration failed: {migrate_err}"))

            except Exception as file_err:
                self.stdout.write(self.style.ERROR(f"[{app}] Unexpected error during restoration: {file_err}"))

        self.stdout.write(self.style.SUCCESS("Restoration completed."))
        