# Generated by Django 4.1.1 on 2022-10-24 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_remove_foodproducts_paircat'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodproducts',
            name='paircategory',
            field=models.ForeignKey(default=19, on_delete=django.db.models.deletion.CASCADE, related_name='_pairedandcategory', to='main.foodcategory'),
        ),
    ]