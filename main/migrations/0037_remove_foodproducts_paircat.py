# Generated by Django 4.1.1 on 2022-10-24 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_foodproducts_paircat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodproducts',
            name='paircat',
        ),
    ]
