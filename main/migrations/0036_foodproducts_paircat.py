# Generated by Django 4.1.1 on 2022-10-24 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_foodproducts1'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodproducts',
            name='paircat',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='_pairedonecategory', to='main.foodcategory'),
        ),
    ]