# Generated by Django 4.1.1 on 2022-10-31 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_menucart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menucart',
            name='event',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.event'),
        ),
    ]