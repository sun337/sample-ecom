# Generated by Django 3.0.8 on 2020-08-03 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20200803_1347'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basket',
            old_name='owner',
            new_name='user',
        ),
    ]
