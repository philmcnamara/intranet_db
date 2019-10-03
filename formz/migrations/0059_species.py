# Generated by Django 2.1.8 on 2019-10-03 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formz', '0058_auto_20190930_1220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latin_name', models.CharField(help_text='Use FULL latin name, e.g. Homo sapiens', max_length=255, verbose_name='latin name')),
                ('common_name', models.CharField(max_length=255, verbose_name='common name')),
                ('show_in_cell_line_collection', models.BooleanField(default=False, verbose_name='show as organism in cell line collection?')),
            ],
            options={
                'verbose_name': 'species',
                'verbose_name_plural': 'species',
                'ordering': ['latin_name', 'common_name'],
            },
        ),
    ]
