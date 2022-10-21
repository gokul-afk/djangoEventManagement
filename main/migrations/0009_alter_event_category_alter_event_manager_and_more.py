# Generated by Django 4.1.1 on 2022-10-21 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_eventcategory_head_alter_event_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_category', to='main.eventcategory'),
        ),
        migrations.AlterField(
            model_name='event',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='eventcategory',
            name='head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
