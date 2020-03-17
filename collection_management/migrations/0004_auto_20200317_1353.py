# Generated by Django 2.2.7 on 2020-03-17 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection_management', '0003_auto_20200317_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalscpombestrain',
            name='box_number',
            field=models.SmallIntegerField(blank=True, verbose_name='box number'),
        ),
        migrations.AlterField(
            model_name='historicalscpombestrain',
            name='frozen_on',
            field=models.DateTimeField(blank=True, default=None, verbose_name='frozen on'),
        ),
        migrations.AlterField(
            model_name='scpombestrain',
            name='box_number',
            field=models.SmallIntegerField(blank=True, verbose_name='box number'),
        ),
        migrations.AlterField(
            model_name='scpombestrain',
            name='frozen_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='frozen_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='scpombestrain',
            name='frozen_on',
            field=models.DateTimeField(blank=True, default=None, verbose_name='frozen on'),
        ),
        migrations.AlterField(
            model_name='scpombestrain',
            name='made_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='made_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
