# Generated by Django 2.1.8 on 2019-07-19 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('formz', '0019_auto_20190719_1650'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StorageLocation',
            new_name='FormZStorageLocation',
        ),
    ]
