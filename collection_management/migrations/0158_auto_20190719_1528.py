# Generated by Django 2.1.8 on 2019-07-19 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection_management', '0157_auto_20190719_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsacerevisiaestrain',
            name='history_gentech_methods',
            field=models.TextField(blank=True, verbose_name='genTech methods'),
        ),
        migrations.AddField(
            model_name='sacerevisiaestrain',
            name='history_gentech_methods',
            field=models.TextField(blank=True, verbose_name='genTech methods'),
        ),
    ]