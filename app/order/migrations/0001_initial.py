# Generated by Django 3.0.8 on 2020-08-02 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0003_auto_20200801_0846'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('currency', models.CharField(default='INR', max_length=12, verbose_name='Currency')),
                ('total', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Order total')),
                ('status', models.CharField(blank=True, choices=[('Created', 'Created - order placed'), ('Processing', 'Processing - order is being processed'), ('Delivered', 'Delivered - order has been successfully delivered'), ('Cancelled', 'Cancelled - order has been cancelled')], default='Open', max_length=100, verbose_name='Status')),
                ('basket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.Basket', verbose_name='Basket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
