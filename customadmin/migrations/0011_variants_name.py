# Generated by Django 4.2 on 2023-07-23 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0010_variantimages_variants_remove_variant_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variants',
            name='name',
            field=models.CharField(default='null', max_length=255),
            preserve_default=False,
        ),
    ]
