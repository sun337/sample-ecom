# Generated by Django 3.0.8 on 2020-08-01 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_line'),
    ]

    operations = [
        migrations.RenameField(
            model_name='line',
            old_name='price_currency',
            new_name='currency',
        ),
    ]
