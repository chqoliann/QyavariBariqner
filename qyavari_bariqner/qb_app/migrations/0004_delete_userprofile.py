# Generated by Django 5.0.7 on 2024-08-07 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qb_app', '0003_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]