# Generated by Django 4.1.1 on 2022-10-24 12:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_remove_foodproducts3_paircat'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodproducts3',
            name='paircat',
            field=models.ForeignKey(blank=True, default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, related_name='_paircat', to='main.foodcategory'),
            preserve_default=False,
        ),
    ]