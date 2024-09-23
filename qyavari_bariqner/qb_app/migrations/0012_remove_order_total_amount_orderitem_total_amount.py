# Generated by Django 4.2.10 on 2024-09-16 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qb_app', '0011_cartitem_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_amount',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]