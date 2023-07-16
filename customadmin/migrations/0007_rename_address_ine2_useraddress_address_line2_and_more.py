# Generated by Django 4.2 on 2023-07-16 06:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0006_useraddress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraddress',
            old_name='address_ine2',
            new_name='address_line2',
        ),
        migrations.AddField(
            model_name='useraddress',
            name='country',
            field=models.CharField(default=django.utils.timezone.now, max_length=30),
            preserve_default=False,
        ),
    ]
