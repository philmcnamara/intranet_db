# Generated by Django 2.2.9 on 2021-02-05 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0011_auto_20210115_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorder',
            name='quantity',
            field=models.IntegerField(verbose_name='quantity'),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(verbose_name='quantity'),
        ),
    ]
