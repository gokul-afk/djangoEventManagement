# Generated by Django 4.1.1 on 2022-10-24 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_foodproducts3'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodproducts',
            name='pair',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.foodproducts'),
        ),
    ]
