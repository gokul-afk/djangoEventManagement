# Generated by Django 4.1.1 on 2022-10-31 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0052_foodcart_pairevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodcart',
            name='pairevent',
        ),
    ]