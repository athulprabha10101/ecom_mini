# Generated by Django 4.2.4 on 2023-08-10 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0025_wishlist_wsihitems'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wsihitems',
            old_name='item',
            new_name='variant',
        ),
        migrations.RemoveField(
            model_name='wsihitems',
            name='quantity',
        ),
    ]
