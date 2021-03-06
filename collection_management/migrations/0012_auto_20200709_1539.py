# Generated by Django 2.2.9 on 2020-07-09 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection_management', '0011_auto_20200709_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalscpombestrain',
            name='comment',
            field=models.CharField(blank=True, max_length=1000, verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='historicalscpombestrain',
            name='frozen_on',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='frozen on'),
        ),
        migrations.AlterField(
            model_name='scpombestrain',
            name='comment',
            field=models.CharField(blank=True, max_length=1000, verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='scpombestrain',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pombe_createdby_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='scpombestrain',
            name='frozen_on',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='frozen on'),
        ),
    ]
