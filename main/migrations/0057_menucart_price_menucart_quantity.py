# Generated by Django 4.1.1 on 2022-11-01 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0056_remove_menucart_price_remove_menucart_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='menucart',
            name='price',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menucart',
            name='quantity',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
