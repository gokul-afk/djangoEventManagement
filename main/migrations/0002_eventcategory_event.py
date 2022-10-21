# Generated by Django 4.1.1 on 2022-10-20 19:57

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=6, unique=True)),
                ('image', models.ImageField(upload_to='event_category/')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', ckeditor.fields.RichTextField()),
                ('scheduled_status', models.BooleanField(default=False)),
                ('venue', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('location', location_field.models.plain.PlainLocationField(max_length=63)),
                ('maximum_attende', models.PositiveIntegerField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(max_length=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.eventcategory')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_updated_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]