# Generated by Django 2.1.8 on 2019-07-19 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection_management', '0155_sacerevisiaestrainepisomalplasmid_destroyed_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sacerevisiaestrainepisomalplasmid',
            name='destroyed_date',
            field=models.DateField(blank=True, null=True, verbose_name='destroyed'),
        ),
    ]
