# Generated by Django 2.2.9 on 2020-12-03 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection_management', '0020_auto_20201203_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaloligo',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='oligo',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
    ]
