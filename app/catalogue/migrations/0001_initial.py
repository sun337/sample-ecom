# Generated by Django 3.0.8 on 2020-07-31 17:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('slug', models.SlugField(max_length=128, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Product class',
                'verbose_name_plural': 'Product classes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_public', models.BooleanField(db_index=True, default=True, help_text='Show this product in search results and catalogue listings.', verbose_name='Is public')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('product_class', models.ForeignKey(blank=True, help_text='Choose what type of product this is', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='catalogue.ProductClass', verbose_name='Product type')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['-created'],
            },
        ),
    ]
