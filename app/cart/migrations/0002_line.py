# Generated by Django 3.0.8 on 2020-07-31 21:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('price_currency', models.CharField(default='INR', max_length=12, verbose_name='Currency')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='Price incl. Tax')),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='cart.Basket', verbose_name='Basket')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_lines', to='catalogue.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Basket line',
                'verbose_name_plural': 'Basket lines',
                'ordering': ['created', 'pk'],
            },
        ),
    ]
