# Generated by Django 2.2.13 on 2021-02-26 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection_management', '0022_auto_20210226_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaloligo',
            name='delivery_email',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicaloligo',
            name='delivery_notification',
            field=models.BooleanField(default=False, verbose_name='Delivery notification?'),
        ),
        migrations.AddField(
            model_name='oligo',
            name='delivery_email',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='oligo',
            name='delivery_notification',
            field=models.BooleanField(default=False, verbose_name='Delivery notification?'),
        ),
    ]
