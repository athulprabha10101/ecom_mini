# Generated by Django 4.2 on 2023-08-03 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0008_orderitems_item_order_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='cancel_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='item_order_status',
            field=models.CharField(choices=[('Processing', 'Processing'), ('Delivered', 'Delivered'), ('Out of delivery', 'Out of delivery'), ('Cancelled', 'Cancelled'), ('Shipped', 'Shipped'), ('Pending', 'Pending')], default='Procrssing', max_length=100),
        ),
    ]
