# Generated by Django 5.1 on 2024-09-25 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qb_app', '0014_userprofile_last_logout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]