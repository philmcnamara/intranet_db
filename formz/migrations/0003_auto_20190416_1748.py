# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-16 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formz', '0002_auto_20190416_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formzbaseelement',
            name='donor_organism',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='donor organism'),
        ),
        migrations.AlterField(
            model_name='formzbaseelement',
            name='nuc_acid_type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='nucleic acid type'),
        ),
    ]