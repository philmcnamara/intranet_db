# Generated by Django 2.1.8 on 2019-08-07 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection_management', '0182_auto_20190806_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecolistrain',
            name='background',
            field=models.CharField(blank=True, choices=[('K12', 'K12'), ('B', 'B')], max_length=255, verbose_name='background'),
        ),
        migrations.AddField(
            model_name='historicalecolistrain',
            name='background',
            field=models.CharField(blank=True, choices=[('K12', 'K12'), ('B', 'B')], max_length=255, verbose_name='background'),
        ),
        migrations.AddField(
            model_name='historicalhuplasmid',
            name='history_formz_ecoli_strains',
            field=models.TextField(blank=True, verbose_name='e. coli strains'),
        ),
        migrations.AddField(
            model_name='huplasmid',
            name='formz_ecoli_strains',
            field=models.ManyToManyField(blank=True, related_name='plasmid_ecoli_strains', to='collection_management.EColiStrain', verbose_name='e. coli strains'),
        ),
        migrations.AddField(
            model_name='huplasmid',
            name='history_formz_ecoli_strains',
            field=models.TextField(blank=True, verbose_name='e. coli strains'),
        ),
    ]
