# Generated by Django 2.1.8 on 2019-10-04 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formz', '0070_auto_20191004_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='species',
            name='name_for_search',
            field=models.CharField(max_length=255),
        ),
    ]