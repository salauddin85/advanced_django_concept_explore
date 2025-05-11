from django.core.management.base import BaseCommand
from django.core.management import call_command
from pathlib import Path
import shutil

class Command(BaseCommand):
    help = 'Restore the latest backup migration for a given app'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='App name to restore migration')

    def handle(self, *args, **kwargs):
        app_name = kwargs['app_name']
        migration_path = Path(f"{app_name}/migrations")
        backup_path = migration_path / "backups"

        if not backup_path.exists():
            self.stdout.write(self.style.ERROR(f"No backup folder found for app: {app_name}"))
            return

        backup_files = sorted(backup_path.glob("*.py"))
        if not backup_files:
            self.stdout.write(self.style.WARNING("No backup files found."))
            return

        latest_backup = backup_files[-1]
        destination = migration_path / latest_backup.name

        # Step 1: Copy back to migrations
        shutil.copy(latest_backup, destination)
        self.stdout.write(self.style.SUCCESS(f"Restored: {latest_backup.name} to {destination}"))

        # Step 2: Run migrate
        call_command("migrate", app_name)
        self.stdout.write(self.style.SUCCESS("Migration applied successfully."))
