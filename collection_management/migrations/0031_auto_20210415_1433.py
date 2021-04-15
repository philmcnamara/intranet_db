# Generated by Django 2.2.18 on 2021-04-15 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection_management', '0030_auto_20210415_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaloligo',
            name='scale_choices',
            field=models.CharField(blank=True, choices=[('25 nmole', '25 nmole'), ('100 nmole', '100 nmole'), ('250 nmole', '250 nmole'), ('1 mmole', '1 mmole'), ('2 mmole', '1 mmole'), ('5 mmole', '5 mmole')], max_length=255, null=True, verbose_name='scale (mole)'),
        ),
        migrations.AddField(
            model_name='oligo',
            name='scale_choices',
            field=models.CharField(blank=True, choices=[('25 nmole', '25 nmole'), ('100 nmole', '100 nmole'), ('250 nmole', '250 nmole'), ('1 mmole', '1 mmole'), ('2 mmole', '1 mmole'), ('5 mmole', '5 mmole')], max_length=255, null=True, verbose_name='scale (mole)'),
        ),
        migrations.AlterField(
            model_name='historicalscpombestrain',
            name='comment',
            field=models.TextField(blank=True, help_text='Any deviation from wild-type (alleles/markers) should be listed in genotype, not comments', verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='scpombestrain',
            name='comment',
            field=models.TextField(blank=True, help_text='Any deviation from wild-type (alleles/markers) should be listed in genotype, not comments', verbose_name='comments'),
        ),
    ]