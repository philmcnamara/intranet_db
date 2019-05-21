# Generated by Django 2.1.8 on 2019-04-26 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection_management', '0087_auto_20190425_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalhuplasmid',
            name='parent_vector',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='collection_management.HuPlasmid', verbose_name='parent vector'),
        ),
        migrations.AlterField(
            model_name='historicalhuplasmid',
            name='vector_zkbs',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='formz.ZkbsPlasmid', verbose_name='ZKBS database vector'),
        ),
        migrations.AlterField(
            model_name='historicalmammalianline',
            name='parental_line',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='collection_management.MammalianLine', verbose_name='parental line'),
        ),
        migrations.AlterField(
            model_name='historicalsacerevisiaestrain',
            name='parent_1',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Main parental strain', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='collection_management.SaCerevisiaeStrain', verbose_name='Parent 1'),
        ),
        migrations.AlterField(
            model_name='historicalsacerevisiaestrain',
            name='parent_2',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Only for crosses', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='collection_management.SaCerevisiaeStrain', verbose_name='Parent 2'),
        ),
        migrations.AlterField(
            model_name='historicalscpombestrain',
            name='parent_1',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Main parental strain', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='collection_management.ScPombeStrain', verbose_name='Parent 1'),
        ),
        migrations.AlterField(
            model_name='historicalscpombestrain',
            name='parent_2',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Only for crosses', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='collection_management.ScPombeStrain', verbose_name='Parent 2'),
        ),
    ]