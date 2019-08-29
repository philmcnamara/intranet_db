# Generated by Django 2.1.8 on 2019-08-26 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formz', '0047_auto_20190806_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='formzproject',
            name='parent_project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='formz.FormZProject', verbose_name='parent project'),
        ),
    ]
