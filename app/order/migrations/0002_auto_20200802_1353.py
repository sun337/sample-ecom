# Generated by Django 3.0.8 on 2020-08-02 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('Created', 'Created - order placed'), ('Processing', 'Processing - order is being processed'), ('Delivered', 'Delivered - order has been successfully delivered'), ('Cancelled', 'Cancelled - order has been cancelled')], default='Created', max_length=100, verbose_name='Status'),
        ),
    ]
