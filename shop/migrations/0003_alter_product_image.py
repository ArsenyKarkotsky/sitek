# Generated by Django 4.1.5 on 2023-04-05 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_news_delete_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='картинка'),
        ),
    ]