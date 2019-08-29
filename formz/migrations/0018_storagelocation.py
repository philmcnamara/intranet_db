# Generated by Django 2.1.8 on 2019-07-19 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('formz', '0017_formzbaseelement_zkbs_oncogene'),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage_location', models.CharField(max_length=255, verbose_name='storage location')),
                ('collection_models', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType', unique=True, verbose_name='collection models')),
            ],
            options={
                'verbose_name': 'storage location',
                'verbose_name_plural': 'storage locations',
            },
        ),
    ]
