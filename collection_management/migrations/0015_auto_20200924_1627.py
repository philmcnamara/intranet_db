# Generated by Django 2.2.9 on 2020-09-24 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection_management', '0014_auto_20200710_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalscpombestrain',
            name='historical_strain',
            field=models.BooleanField(default=False, help_text='Strain exists in Germany', verbose_name='historical strain'),
        ),
        migrations.AddField(
            model_name='scpombestrain',
            name='historical_strain',
            field=models.BooleanField(default=False, help_text='Strain exists in Germany', verbose_name='historical strain'),
        ),
    ]