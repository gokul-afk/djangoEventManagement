# Generated by Django 4.1.1 on 2022-10-24 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_foodcart'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodproducts',
            name='pair',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.foodproducts'),
        ),
        migrations.AddField(
            model_name='foodproducts',
            name='paircat',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.foodcategory'),
        ),
        migrations.AlterField(
            model_name='foodproducts',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='food_category', to='main.foodcategory'),
        ),
    ]
