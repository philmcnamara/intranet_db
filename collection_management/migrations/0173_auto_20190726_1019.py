# Generated by Django 2.1.8 on 2019-07-26 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection_management', '0172_auto_20190723_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalhuplasmid',
            name='vector_zkbs',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='<a href="/formz/zkbsplasmid/" target="_blank">View all</a>', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='formz.ZkbsPlasmid', verbose_name='ZKBS database vector'),
        ),
        migrations.AlterField(
            model_name='historicalmammalianline',
            name='zkbs_cell_line',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='<a href="/formz/zkbscellline/" target="_blank">View all</a>', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='formz.ZkbsCellLine', verbose_name='ZKBS database cell line'),
        ),
        migrations.AlterField(
            model_name='huplasmid',
            name='formz_elements',
            field=models.ManyToManyField(blank=True, help_text='<a href="/formz/formzbaseelement/" target="_blank">View all/Change</a>', to='formz.FormZBaseElement', verbose_name='elements'),
        ),
        migrations.AlterField(
            model_name='huplasmid',
            name='vector_zkbs',
            field=models.ForeignKey(blank=True, help_text='<a href="/formz/zkbsplasmid/" target="_blank">View all</a>', null=True, on_delete=django.db.models.deletion.PROTECT, to='formz.ZkbsPlasmid', verbose_name='ZKBS database vector'),
        ),
        migrations.AlterField(
            model_name='mammalianline',
            name='zkbs_cell_line',
            field=models.ForeignKey(blank=True, help_text='<a href="/formz/zkbscellline/" target="_blank">View all</a>', null=True, on_delete=django.db.models.deletion.PROTECT, to='formz.ZkbsCellLine', verbose_name='ZKBS database cell line'),
        ),
        migrations.AlterField(
            model_name='sacerevisiaestrain',
            name='formz_elements',
            field=models.ManyToManyField(blank=True, help_text='Use only when an element is not present in the chosen plasmid(s), if any. <a href="/formz/formzbaseelement/" target="_blank">View all/Change</a>', related_name='cerevisiae_formz_element', to='formz.FormZBaseElement', verbose_name='elements'),
        ),
        migrations.AlterField(
            model_name='scpombestrain',
            name='formz_elements',
            field=models.ManyToManyField(blank=True, help_text='Use only when an element is not present in the chosen plasmid(s), if any. <a href="/formz/formzbaseelement/" target="_blank">View all/Change</a>', related_name='pombe_formz_element', to='formz.FormZBaseElement', verbose_name='elements'),
        ),
    ]
