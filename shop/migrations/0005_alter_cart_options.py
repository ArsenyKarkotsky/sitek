# Generated by Django 4.1.5 on 2023-04-06 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_cart_cartitem_cart_products_cart_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'карзина', 'verbose_name_plural': 'карзины'},
        ),
    ]