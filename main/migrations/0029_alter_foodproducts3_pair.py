# Generated by Django 4.1.1 on 2022-10-24 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_foodproducts_pair'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodproducts3',
            name='pair',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.foodproducts3'),
        ),
    ]
