# Generated by Django 4.2.10 on 2024-09-17 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qb_app', '0012_remove_order_total_amount_orderitem_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_activity',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]