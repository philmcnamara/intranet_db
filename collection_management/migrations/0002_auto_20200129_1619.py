# Generated by Django 2.2.7 on 2020-01-29 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('formz', '0001_initial'),
        ('collection_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='scpombestrainepisomalplasmid',
            name='formz_projects',
            field=models.ManyToManyField(blank=True, related_name='pombe_episomal_plasmid_projects', to='formz.FormZProject'),
        ),
        migrations.AddField(
            model_name='scpombestrainepisomalplasmid',
            name='plasmid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='collection_management.Plasmid', verbose_name='Plasmid'),
        ),
        migrations.AddField(
            model_name='scpombestrainepisomalplasmid',
            name='scpombe_strain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='collection_management.ScPombeStrain'),
        ),
        migrations.AddField(
            model_name='scpombestrain',
            name='approval_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pombe_approval_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='scpombestrain',
            name='cassette_plasmids',
            field=models.ManyToManyField(blank=True, help_text='Tagging and knock out plasmids', related_name='pombe_cassette_plasmids', to='collection_management.Plasmid'),
        ),
        migrations.AddField(
            model_name='scpombestrain',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pombe_createdby_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='scpombestrain',
            name='episomal_plasmids',
            field=models.ManyToManyField(blank=True, related_name='pombe_episomal_plasmids', through='collection_management.ScPombeStrainEpisomalPlasmid', to='collection_management.Plasmid'),
        ),
        migrations.AddField(
            model_name='scpombestrain',
            name='formz_elements',
            field=models.ManyToManyField(blank=True, help_text='Use only when an element is not present in the chosen plasmid(s), if any. <a href="/formz/formzbaseelement/" target="_blank">View all/Change</a>', related_name='pombe_formz_element', to='formz.FormZBaseElement', verbose_name='elements'),
        ),
        migrations.AddField(
            model_name='scpombestrain',
            name='formz_gentech_methods',
            field=models.ManyToManyField(blank=True, help_text='The methods used to create the strain', related_name='pombe_gentech_method', to='formz.GenTechMethod', verbose_name='genTech methods'),
        ),
        migrations.AddField(
            model_name='scpombestrain',
            name='formz_projects',
            field=models.ManyToManyField(related_name='pombe_formz_project', to='formz.FormZProject', verbose_name='formZ projects'),
        ),
        migrations.AddField(
            model_name='scpombestrain',
            name='integrated_plasmids',
            field=models.ManyToManyField(blank=True, related_name='pombe_integrated_plasmids', to='collection_management.Plasmid'),
        ),
        migrations.AddField(
            model_name='scpombestrain',
            name='parent_1',
            field=models.ForeignKey(blank=True, help_text='Main parental strain', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pombe_parent_1', to='collection_management.ScPombeStrain', verbose_name='Parent 1'),
        ),
        migrations.AddField(
            model_name='scpombestrain',
            name='parent_2',
            field=models.ForeignKey(blank=True, help_text='Only for crosses', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pombe_parent_2', to='collection_management.ScPombeStrain', verbose_name='Parent 2'),
        ),
        migrations.AddField(
            model_name='sacerevisiaestrainepisomalplasmid',
            name='formz_projects',
            field=models.ManyToManyField(blank=True, related_name='cerevisiae_episomal_plasmid_projects', to='formz.FormZProject'),
        ),
        migrations.AddField(
            model_name='sacerevisiaestrainepisomalplasmid',
            name='plasmid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='collection_management.Plasmid', verbose_name='Plasmid'),
        ),
        migrations.AddField(
            model_name='sacerevisiaestrainepisomalplasmid',
            name='sacerevisiae_strain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='collection_management.SaCerevisiaeStrain'),
        ),
        migrations.AddField(
            model_name='sacerevisiaestrain',
            name='approval_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cerevisiae_approval_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sacerevisiaestrain',
            name='cassette_plasmids',
            field=models.ManyToManyField(blank=True, help_text='Tagging and knock out plasmids', related_name='cerevisiae_cassette_plasmids', to='collection_management.Plasmid'),
        ),
        migrations.AddField(
            model_name='sacerevisiaestrain',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cerevisiae_createdby_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sacerevisiaestrain',
            name='episomal_plasmids',
            field=models.ManyToManyField(blank=True, related_name='cerevisiae_episomal_plasmids', through='collection_management.SaCerevisiaeStrainEpisomalPlasmid', to='collection_management.Plasmid'),
        ),
        migrations.AddField(
            model_name='sacerevisiaestrain',
            name='formz_elements',
            field=models.ManyToManyField(blank=True, help_text='Use only when an element is not present in the chosen plasmid(s), if any. <a href="/formz/formzbaseelement/" target="_blank">View all/Change</a>', related_name='cerevisiae_formz_element', to='formz.FormZBaseElement', verbose_name='elements'),
        ),
        migrations.AddField(
            model_name='sacerevisiaestrain',
            name='formz_gentech_methods',
            field=models.ManyToManyField(blank=True, help_text='The methods used to create the strain', related_name='cerevisiae_gentech_method', to='formz.GenTechMethod', verbose_name='genTech methods'),
        ),
        migrations.AddField(
            model_name='sacerevisiaestrain',
            name='formz_projects',
            field=models.ManyToManyField(related_name='cerevisiae_formz_project', to='formz.FormZProject', verbose_name='projects'),
        ),
        migrations.AddField(
            model_name='sacerevisiaestrain',
            name='integrated_plasmids',
            field=models.ManyToManyField(blank=True, related_name='cerevisiae_integrated_plasmids', to='collection_management.Plasmid'),
        ),
        migrations.AddField(
            model_name='sacerevisiaestrain',
            name='parent_1',
            field=models.ForeignKey(blank=True, help_text='Main parental strain', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cerevisiae_parent_1', to='collection_management.SaCerevisiaeStrain', verbose_name='Parent 1'),
        ),
        migrations.AddField(
            model_name='sacerevisiaestrain',
            name='parent_2',
            field=models.ForeignKey(blank=True, help_text='Only for crosses', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cerevisiae_parent_2', to='collection_management.SaCerevisiaeStrain', verbose_name='Parent 2'),
        ),
        migrations.AddField(
            model_name='plasmid',
            name='approval_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='plasmid_approval_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='plasmid',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='plasmid_createdby_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='plasmid',
            name='formz_ecoli_strains',
            field=models.ManyToManyField(related_name='plasmid_ecoli_strains', to='collection_management.EColiStrain', verbose_name='e. coli strains'),
        ),
        migrations.AddField(
            model_name='plasmid',
            name='formz_elements',
            field=models.ManyToManyField(blank=True, help_text='<a href="/formz/formzbaseelement/" target="_blank">View all/Change</a>', to='formz.FormZBaseElement', verbose_name='elements'),
        ),
        migrations.AddField(
            model_name='plasmid',
            name='formz_gentech_methods',
            field=models.ManyToManyField(blank=True, help_text='The methods used to create the plasmid', related_name='plasmid_gentech_method', to='formz.GenTechMethod', verbose_name='genTech methods'),
        ),
        migrations.AddField(
            model_name='plasmid',
            name='formz_projects',
            field=models.ManyToManyField(related_name='plasmid_formz_projects', to='formz.FormZProject', verbose_name='projects'),
        ),
        migrations.AddField(
            model_name='plasmid',
            name='parent_vector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='plasmid_parent_vector', to='collection_management.Plasmid', verbose_name='parent vector'),
        ),
        migrations.AddField(
            model_name='plasmid',
            name='vector_zkbs',
            field=models.ForeignKey(help_text='The backbone of the plasmid, from the ZKBS database. If not applicable, choose none. <a href="/formz/zkbsplasmid/" target="_blank">View all</a>', null=True, on_delete=django.db.models.deletion.PROTECT, to='formz.ZkbsPlasmid', verbose_name='ZKBS database vector'),
        ),
        migrations.AddField(
            model_name='oligo',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='oligo_createdby_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalscpombestrain',
            name='approval_user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalscpombestrain',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalscpombestrain',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalscpombestrain',
            name='parent_1',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Main parental strain', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='collection_management.ScPombeStrain', verbose_name='Parent 1'),
        ),
        migrations.AddField(
            model_name='historicalscpombestrain',
            name='parent_2',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Only for crosses', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='collection_management.ScPombeStrain', verbose_name='Parent 2'),
        ),
        migrations.AddField(
            model_name='historicalsacerevisiaestrain',
            name='approval_user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalsacerevisiaestrain',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalsacerevisiaestrain',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalsacerevisiaestrain',
            name='parent_1',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Main parental strain', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='collection_management.SaCerevisiaeStrain', verbose_name='Parent 1'),
        ),
        migrations.AddField(
            model_name='historicalsacerevisiaestrain',
            name='parent_2',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Only for crosses', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='collection_management.SaCerevisiaeStrain', verbose_name='Parent 2'),
        ),
        migrations.AddField(
            model_name='historicalplasmid',
            name='approval_user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalplasmid',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalplasmid',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalplasmid',
            name='parent_vector',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='collection_management.Plasmid', verbose_name='parent vector'),
        ),
        migrations.AddField(
            model_name='historicalplasmid',
            name='vector_zkbs',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='The backbone of the plasmid, from the ZKBS database. If not applicable, choose none. <a href="/formz/zkbsplasmid/" target="_blank">View all</a>', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='formz.ZkbsPlasmid', verbose_name='ZKBS database vector'),
        ),
        migrations.AddField(
            model_name='historicaloligo',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaloligo',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalecolistrain',
            name='approval_user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalecolistrain',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalecolistrain',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcellline',
            name='approval_user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcellline',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcellline',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcellline',
            name='organism',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='formz.Species', verbose_name='organism'),
        ),
        migrations.AddField(
            model_name='historicalcellline',
            name='parental_line',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='collection_management.CellLine', verbose_name='parental line'),
        ),
        migrations.AddField(
            model_name='historicalcellline',
            name='zkbs_cell_line',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='If not applicable, choose none. <a href="/formz/zkbscellline/" target="_blank">View all</a>', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='formz.ZkbsCellLine', verbose_name='ZKBS database cell line'),
        ),
        migrations.AddField(
            model_name='historicalantibody',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalantibody',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ecolistrain',
            name='approval_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='coli_approval_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ecolistrain',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='coli_createdby_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ecolistrain',
            name='formz_elements',
            field=models.ManyToManyField(blank=True, related_name='coli_formz_element', to='formz.FormZBaseElement', verbose_name='elements'),
        ),
        migrations.AddField(
            model_name='ecolistrain',
            name='formz_projects',
            field=models.ManyToManyField(related_name='coli_formz_project', to='formz.FormZProject', verbose_name='formZ projects'),
        ),
        migrations.AddField(
            model_name='celllineepisomalplasmid',
            name='cell_line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='collection_management.CellLine'),
        ),
        migrations.AddField(
            model_name='celllineepisomalplasmid',
            name='formz_projects',
            field=models.ManyToManyField(blank=True, related_name='cellline_episomal_plasmid_projects', to='formz.FormZProject'),
        ),
        migrations.AddField(
            model_name='celllineepisomalplasmid',
            name='plasmid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='collection_management.Plasmid', verbose_name='Plasmid'),
        ),
        migrations.AddField(
            model_name='celllinedoc',
            name='cell_line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='collection_management.CellLine'),
        ),
        migrations.AddField(
            model_name='cellline',
            name='approval_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cellline_approval_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cellline',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cellline_createdby_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cellline',
            name='episomal_plasmids',
            field=models.ManyToManyField(blank=True, related_name='cellline_episomal_plasmids', through='collection_management.CellLineEpisomalPlasmid', to='collection_management.Plasmid'),
        ),
        migrations.AddField(
            model_name='cellline',
            name='formz_elements',
            field=models.ManyToManyField(blank=True, help_text='Use only when an element is not present in the chosen plasmid(s), if any', related_name='cellline_formz_element', to='formz.FormZBaseElement', verbose_name='elements'),
        ),
        migrations.AddField(
            model_name='cellline',
            name='formz_gentech_methods',
            field=models.ManyToManyField(blank=True, help_text='The methods used to create the cell line', related_name='cellline_gentech_method', to='formz.GenTechMethod', verbose_name='genTech methods'),
        ),
        migrations.AddField(
            model_name='cellline',
            name='formz_projects',
            field=models.ManyToManyField(related_name='cellline_zprojects', to='formz.FormZProject', verbose_name='projects'),
        ),
        migrations.AddField(
            model_name='cellline',
            name='integrated_plasmids',
            field=models.ManyToManyField(blank=True, related_name='cellline_integrated_plasmids', to='collection_management.Plasmid'),
        ),
        migrations.AddField(
            model_name='cellline',
            name='organism',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='formz.Species', verbose_name='organism'),
        ),
        migrations.AddField(
            model_name='cellline',
            name='parental_line',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='collection_management.CellLine', verbose_name='parental line'),
        ),
        migrations.AddField(
            model_name='cellline',
            name='zkbs_cell_line',
            field=models.ForeignKey(help_text='If not applicable, choose none. <a href="/formz/zkbscellline/" target="_blank">View all</a>', null=True, on_delete=django.db.models.deletion.PROTECT, to='formz.ZkbsCellLine', verbose_name='ZKBS database cell line'),
        ),
        migrations.AddField(
            model_name='antibody',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
