# Generated by Django 2.2.9 on 2021-01-08 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0002_auto_20210108_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalorder',
            name='email_sent',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='email_sent',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
