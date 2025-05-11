# from django.core.management.base import BaseCommand
# from django.db import connection
# from pathlib import Path
# import os
# import shutil

# class Command(BaseCommand):
#     help = 'Rollback the latest migration and keep a backup'

#     def add_arguments(self, parser):
#         parser.add_argument('app_name', type=str, help='App name to reset last migration')

#     def handle(self, *args, **kwargs):
#         app_name = kwargs['app_name']
#         migration_path = Path(f"{app_name}/migrations")
#         backup_path = migration_path / 'backups'

#         if not migration_path.exists():
#             self.stdout.write(self.style.ERROR(f"No migrations folder found for app: {app_name}"))
#             return

#         # init.py without file in migration
#         migration_files = sorted([
#             f for f in migration_path.glob('*.py') if f.name != '__init__.py'
#         ])

#         if not migration_files:
#             self.stdout.write(self.style.WARNING("No migration files found."))
#             return

#         # last migration file
#         last_migration_file = migration_files[-1]
#         last_migration_name = last_migration_file.stem

#         # Step 1: BACKUP
#         backup_path.mkdir(exist_ok=True)
#         shutil.copy(last_migration_file, backup_path / last_migration_file.name)
#         self.stdout.write(self.style.NOTICE(f"Backup created at: {backup_path/last_migration_file.name}"))

#         # Step 2: Reverse migration
#         from django.core.management import call_command
#         revert_to = migration_files[-2].stem.split('_')[0] if len(migration_files) > 1 else 'zero'
#         call_command("migrate", app_name, revert_to)
#         self.stdout.write(self.style.SUCCESS(f"Rolled back to: {revert_to}"))

#         # Step 3: Delete the file
#         os.remove(last_migration_file)
#         self.stdout.write(self.style.SUCCESS(f"Deleted migration file: {last_migration_file.name}"))

#         #  Step 4: Remove from DB
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "DELETE FROM django_migrations WHERE app = %s AND name = %s",
#                 [app_name, last_migration_name]
#             )
#         self.stdout.write(self.style.SUCCESS("Migration entry removed from DB."))




# dependencies migration file delete
# ---------------------------------------------------------------------------------
from django.core.management.base import BaseCommand
from django.db.migrations.loader import MigrationLoader
from django.db import connection
from django.core.management import call_command
from pathlib import Path
import os
import shutil


class Command(BaseCommand):
    help = 'Rollback the latest migration (with dependencies) and backup safely'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='App name to rollback migration from')

    def handle(self, *args, **kwargs):
        app_name = kwargs['app_name']

        try:
            loader = MigrationLoader(connection)
            graph = loader.graph

            leaf_nodes = graph.leaf_nodes(app_name)
            if not leaf_nodes:
                self.stdout.write(self.style.WARNING(f"No migrations found for app: {app_name}"))
                return

            target_node = leaf_nodes[-1]
            rollback_plan = graph.forwards_plan(target_node)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading migration graph: {str(e)}"))
            return

        rollback_apps = []
        for app_label, migration_name in rollback_plan:
            if app_label not in rollback_apps:
                rollback_apps.append(app_label)
        rollback_apps = rollback_apps[::-1]

        for app in rollback_apps:
            try:
                migration_path = Path(f"{app}/migrations")
                backup_path = migration_path / 'backups'

                if not migration_path.exists():
                    self.stdout.write(self.style.WARNING(f"No migrations folder for: {app}"))
                    continue

                migration_files = sorted([
                    f for f in migration_path.glob('*.py') if f.name != '__init__.py'
                ])

                if not migration_files:
                    self.stdout.write(self.style.WARNING(f"No migration files in: {app}"))
                    continue

                last_migration_file = migration_files[-1]
                last_migration_name = last_migration_file.stem

                # Step 1: Backup
                backup_path.mkdir(exist_ok=True)
                shutil.copy(last_migration_file, backup_path / last_migration_file.name)
                self.stdout.write(self.style.NOTICE(f"[{app}] Backup: {backup_path / last_migration_file.name}"))

                # Step 2: Revert migration
                if len(migration_files) > 1:
                    revert_to = migration_files[-2].stem
                else:
                    revert_to = 'zero'

                call_command("migrate", app, revert_to)
                self.stdout.write(self.style.SUCCESS(f"[{app}] Rolled back to: {revert_to}"))

                # Step 3: Delete migration file
                os.remove(last_migration_file)
                self.stdout.write(self.style.SUCCESS(f"[{app}] Deleted migration: {last_migration_file.name}"))

                # Step 4: Remove from DB
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM django_migrations WHERE app = %s AND name = %s",
                        [app, last_migration_name]
                    )
                self.stdout.write(self.style.SUCCESS(f"[{app}] Removed migration from DB."))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"[{app}] Error: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("Rollback completed."))