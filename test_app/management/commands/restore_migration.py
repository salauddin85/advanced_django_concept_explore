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
    help = 'Restore last migration file from backup and apply migration (with dependencies)'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='App name to restore migration')

    def handle(self, *args, **kwargs):
        app_name = kwargs['app_name']
        loader = MigrationLoader(connection)
        graph = loader.graph

        try:
            rollback_plan = graph.forwards_plan((app_name, graph.leaf_nodes(app_name)[-1]))
        except IndexError:
            rollback_plan = []

        # Reverse order for restoring
        rollback_apps = []
        for app_label, _ in rollback_plan:
            if app_label not in rollback_apps:
                rollback_apps.append(app_label)
        rollback_apps = rollback_apps[::-1]

        # Always include the requested app first if no dependency found
        if app_name not in rollback_apps:
            rollback_apps.insert(0, app_name)

        for app in rollback_apps:
            migration_path = Path(f"{app}/migrations")
            backup_path = migration_path / "backups"

            if not backup_path.exists():
                self.stdout.write(self.style.WARNING(f"[{app}] No backup folder found. Skipping."))
                continue

            backup_files = sorted(backup_path.glob("*.py"))
            if not backup_files:
                self.stdout.write(self.style.WARNING(f"[{app}] No backup files found."))
                continue

            latest_backup = backup_files[-1]
            destination = migration_path / latest_backup.name

            # Step 1: Copy back to migrations
            shutil.copy(latest_backup, destination)
            self.stdout.write(self.style.SUCCESS(f"[{app}] Restored: {latest_backup.name}"))

            # Step 2: Run migrate
            call_command("migrate", app)
            self.stdout.write(self.style.SUCCESS(f"[{app}] Migration applied."))
