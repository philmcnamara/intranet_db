# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-13 07:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0033_costunit_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costunit',
            name='description',
            field=models.CharField(max_length=255, unique=True, verbose_name='Description'),
        ),
    ]