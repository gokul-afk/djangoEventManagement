# Generated by Django 4.1.1 on 2022-10-25 10:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_delete_foodproducts1'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventimage',
            name='type',
            field=models.CharField(default=django.utils.timezone.now, max_length=300),
            preserve_default=False,
        ),
    ]
