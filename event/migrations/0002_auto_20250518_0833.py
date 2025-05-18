from django.db import migrations
from datetime import datetime

def add_initial_events(apps, schema_editor):
    Event = apps.get_model('event', 'Event')
    Team = apps.get_model('test_app', 'Team')  # team ফরেিনকি
    Management = apps.get_model('test_app', 'Management')  # management ফরেিনকি
    User = apps.get_model('auth', 'User')  # ইউজার মডেল
    
    team = Team.objects.first()
    management = Management.objects.first()
    user = User.objects.first()

    if team and management and user:
        event1 = Event.objects.create(
            name="Sample Event",
            date=datetime(2025, 5, 30, 10, 0),
            location="Dhaka",
            team=team,
            management=management,
            description="This is a sample event.",
            is_active=True
        )
        event1.attendees.add(user)

        event2 = Event.objects.create(
            name="Sample2 Event",
            date=datetime(2025, 9, 30, 10, 0),
            location="Dhaka Mirpur",
            team=team,
            management=management,
            description="This is a sample event 2.",
            is_active=True
        )
        event2.attendees.add(user)
        event3 = Event.objects.create(
            name="Sample3 Event",
            date=datetime(2025, 10, 30, 10, 0),
            location="Dhaka Uttara",
            team=team,
            management=management,
            description="This is a sample event 3.",
            is_active=True
        )
        event3.attendees.add(user)

class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),  # আগের মাইগ্রেশন ফাইল
    ]

    operations = [
        migrations.RunPython(add_initial_events),
    ]
