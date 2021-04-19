# Generated by Django 2.2.18 on 2021-04-19 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection_management', '0031_auto_20210415_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaloligo',
            name='scale_choices',
            field=models.CharField(blank=True, choices=[('25 nmole', '25 nmole'), ('100 nmole', '100 nmole'), ('250 nmole', '250 nmole'), ('1 µmole', '1 µmole'), ('2 µmole', '2 µmole'), ('5 µmole', '5 µmole')], max_length=255, null=True, verbose_name='scale (mole)'),
        ),
        migrations.AlterField(
            model_name='oligo',
            name='scale_choices',
            field=models.CharField(blank=True, choices=[('25 nmole', '25 nmole'), ('100 nmole', '100 nmole'), ('250 nmole', '250 nmole'), ('1 µmole', '1 µmole'), ('2 µmole', '2 µmole'), ('5 µmole', '5 µmole')], max_length=255, null=True, verbose_name='scale (mole)'),
        ),
    ]
