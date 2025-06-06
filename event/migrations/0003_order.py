# Generated by Django 5.1.5 on 2025-05-18 09:42

import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20250518_0833'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
            ],
        ),
    ]
