# Generated by Django 4.2 on 2023-08-07 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0015_orders_applied_coupon_alter_coupons_coupon_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='applied_coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customadmin.coupons'),
        ),
    ]