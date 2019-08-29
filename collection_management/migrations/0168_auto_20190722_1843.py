# Generated by Django 2.1.8 on 2019-07-22 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection_management', '0167_auto_20190722_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sacerevisiaestrain',
            name='formz_elements',
            field=models.ManyToManyField(blank=True, help_text='Use only when an element is not present in one of the above-chosen plasmid(s), if any. <a href="/formz/formzbaseelement/" target="_blank">View/Change elements</a>', related_name='cerevisiae_formz_element', to='formz.FormZBaseElement', verbose_name='elements'),
        ),
        migrations.AlterField(
            model_name='scpombestrain',
            name='formz_elements',
            field=models.ManyToManyField(blank=True, help_text='Use only when an element is not present in one of the above-chosen plasmid(s), if any. <a href="/formz/formzbaseelement/" target="_blank">View/Change elements</a>', related_name='pombe_formz_element', to='formz.FormZBaseElement', verbose_name='elements'),
        ),
    ]
