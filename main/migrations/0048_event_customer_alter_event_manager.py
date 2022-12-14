# Generated by Django 4.1.1 on 2022-10-31 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_userprofile_is_pass_alter_userprofile_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_manager', to=settings.AUTH_USER_MODEL),
        ),
    ]
