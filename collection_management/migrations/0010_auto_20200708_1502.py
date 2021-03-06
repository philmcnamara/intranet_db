# Generated by Django 2.2.9 on 2020-07-08 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collection_management', '0009_auto_20200708_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaloligo',
            name='ordered_by',
        ),
        migrations.RemoveField(
            model_name='oligo',
            name='ordered_by',
        ),
        migrations.AddField(
            model_name='historicaloligo',
            name='ordered_by_user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='oligo',
            name='ordered_by_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
