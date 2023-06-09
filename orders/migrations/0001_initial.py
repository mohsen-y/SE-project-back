# Generated by Django 4.2 on 2023-06-01 18:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=10)),
                ('shipping_fee', models.PositiveIntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('transaction_id', models.UUIDField()),
                ('transaction_code', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('shaparak_reference_id', models.CharField(blank=True, max_length=15, null=True)),
                ('card_number', models.CharField(blank=True, max_length=16, null=True)),
                ('datetime', models.DateTimeField()),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='orders.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('black', 'Black'), ('white', 'White'), ('green', 'Green'), ('blue', 'Blue'), ('red', 'Red')], max_length=10)),
                ('size', models.PositiveSmallIntegerField()),
                ('quantity', models.PositiveSmallIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'unique_together': {('order', 'product', 'color', 'size')},
            },
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', through='orders.OrderProduct', to='products.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
