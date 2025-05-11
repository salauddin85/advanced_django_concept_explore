from django.core.management.base import BaseCommand
from django.db import connection
from pathlib import Path
import os
import shutil

class Command(BaseCommand):
    help = 'Rollback the latest migration and keep a backup'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='App name to reset last migration')

    def handle(self, *args, **kwargs):
        app_name = kwargs['app_name']
        migration_path = Path(f"{app_name}/migrations")
        backup_path = migration_path / 'backups'

        if not migration_path.exists():
            self.stdout.write(self.style.ERROR(f"No migrations folder found for app: {app_name}"))
            return

        # init.py without file in migration
        migration_files = sorted([
            f for f in migration_path.glob('*.py') if f.name != '__init__.py'
        ])

        if not migration_files:
            self.stdout.write(self.style.WARNING("No migration files found."))
            return

        # last migration file
        last_migration_file = migration_files[-1]
        last_migration_name = last_migration_file.stem

        # Step 1: BACKUP
        backup_path.mkdir(exist_ok=True)
        shutil.copy(last_migration_file, backup_path / last_migration_file.name)
        self.stdout.write(self.style.NOTICE(f"Backup created at: {backup_path/last_migration_file.name}"))

        # Step 2: Reverse migration
        from django.core.management import call_command
        revert_to = migration_files[-2].stem.split('_')[0] if len(migration_files) > 1 else 'zero'
        call_command("migrate", app_name, revert_to)
        self.stdout.write(self.style.SUCCESS(f"Rolled back to: {revert_to}"))

        # Step 3: Delete the file
        os.remove(last_migration_file)
        self.stdout.write(self.style.SUCCESS(f"Deleted migration file: {last_migration_file.name}"))

        #  Step 4: Remove from DB
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM django_migrations WHERE app = %s AND name = %s",
                [app_name, last_migration_name]
            )
        self.stdout.write(self.style.SUCCESS("Migration entry removed from DB."))
