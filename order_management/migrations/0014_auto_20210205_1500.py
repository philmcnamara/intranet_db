# Generated by Django 2.2.9 on 2021-02-05 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0013_auto_20210205_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalorder',
            name='cost_unit',
        ),
        migrations.RemoveField(
            model_name='order',
            name='cost_unit',
        ),
        migrations.AlterField(
            model_name='historicalorder',
            name='primary_location',
            field=models.CharField(blank=True, help_text="Please update with item's location after it arrives", max_length=255, verbose_name='primary location'),
        ),
        migrations.AlterField(
            model_name='order',
            name='primary_location',
            field=models.CharField(blank=True, help_text="Please update with item's location after it arrives", max_length=255, verbose_name='primary location'),
        ),
        migrations.DeleteModel(
            name='CostUnit',
        ),
    ]
