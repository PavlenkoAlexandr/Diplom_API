# Generated by Django 3.1.2 on 2021-03-17 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('text', models.TextField()),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCollectionPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('Collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collection_positions', to='product_collections.collection')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='collection',
            name='positions',
            field=models.ManyToManyField(through='product_collections.ProductCollectionPosition', to='products.Product'),
        ),
    ]
