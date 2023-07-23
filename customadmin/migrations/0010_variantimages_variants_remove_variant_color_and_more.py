# Generated by Django 4.2 on 2023-07-23 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0009_product_productimages_variant_variation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariantImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images')),
            ],
        ),
        migrations.CreateModel(
            name='Variants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('original_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='variant',
            name='color',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='product',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='storage',
        ),
        migrations.RenameModel(
            old_name='Product',
            new_name='BaseProducts',
        ),
        migrations.RenameModel(
            old_name='Variation',
            new_name='Variations',
        ),
        migrations.DeleteModel(
            name='ProductImages',
        ),
        migrations.DeleteModel(
            name='Variant',
        ),
        migrations.AddField(
            model_name='variants',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant', to='customadmin.baseproducts'),
        ),
        migrations.AddField(
            model_name='variants',
            name='variation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='customadmin.variations'),
        ),
        migrations.AddField(
            model_name='variantimages',
            name='variation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant_images', to='customadmin.variations'),
        ),
    ]
