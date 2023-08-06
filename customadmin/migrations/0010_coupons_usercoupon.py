# Generated by Django 4.2 on 2023-08-04 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0009_orderitems_cancel_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_with_this_coupon', to='customadmin.coupons')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coupons_of_this_user', to='customadmin.userprofile')),
            ],
        ),
    ]
