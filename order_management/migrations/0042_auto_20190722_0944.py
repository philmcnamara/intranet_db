# Generated by Django 2.1.8 on 2019-07-22 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0041_auto_20190718_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msdsform',
            name='name',
            field=models.FileField(help_text='max. 2 MB', unique=True, upload_to='order_management/msdsform/', verbose_name='file name'),
        ),
        migrations.AlterField(
            model_name='orderextradoc',
            name='name',
            field=models.FileField(help_text='max. 2 MB', upload_to='temp/', verbose_name='file name'),
        ),
    ]
