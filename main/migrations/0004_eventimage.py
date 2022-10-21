# Generated by Django 4.1.1 on 2022-10-20 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_event_location_alter_eventcategory_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='event_image/')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.event')),
            ],
        ),
    ]