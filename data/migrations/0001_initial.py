# Generated by Django 3.2 on 2023-07-03 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib_Batiment', models.CharField(db_column='lib_Batiment', max_length=120)),
                ('nb_logts', models.PositiveIntegerField(db_column='nb_logts')),
                ('nb_etage', models.PositiveIntegerField(db_column='nb_etage')),
                ('date_joined', models.DateTimeField(auto_now_add=True, db_column='date_joined', verbose_name='date joined')),
            ],
            options={
                'db_table': 'data_batiment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib_Cite', models.CharField(db_column='lib_Cite', max_length=120)),
                ('nb_logts', models.PositiveIntegerField(db_column='nb_logts')),
                ('date_joined', models.DateTimeField(auto_now_add=True, db_column='date_joined', verbose_name='date joined')),
            ],
            options={
                'db_table': 'data_cite',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mois', models.PositiveIntegerField(db_column='mois')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at')),
                ('total', models.FloatField(db_column='total')),
            ],
            options={
                'db_table': 'data_consultation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Contrat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_cnt', models.DateTimeField(db_column='date_cnt', null=True)),
                ('date_strt_loyer', models.DateTimeField(db_column='date_strt_loyer', null=True)),
                ('loyer', models.FloatField(db_column='loyer')),
                ('charge', models.CharField(db_column='charge', max_length=120)),
                ('mnt_tva', models.FloatField(db_column='mnt_tva')),
                ('total_of_month', models.FloatField(db_column='total_of_month', default=0)),
            ],
            options={
                'db_table': 'data_contrat',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Logement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surface', models.FloatField(db_column='surface', default='m2')),
                ('prix_logement', models.FloatField(db_column='prix_logement')),
                ('type_logement', models.CharField(db_column='type_logement', max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at')),
            ],
            options={
                'db_table': 'data_logement',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Occupant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oc_id', models.PositiveIntegerField(db_column='oc_id', unique=True)),
                ('nom_oc', models.CharField(db_column='nom_oc', max_length=120)),
                ('prenom_oc', models.CharField(db_column='prenom_oc', max_length=120)),
                ('date_naiss', models.DateTimeField(db_column='date_naiss', null=True)),
                ('lieu_naiss', models.CharField(db_column='lieu_naiss', max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at')),
            ],
            options={
                'db_table': 'data_occupant',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Unite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib_unit', models.CharField(db_column='lib_unit', max_length=120)),
                ('date_joined', models.DateTimeField(auto_now_add=True, db_column='date_joined', verbose_name='date joined')),
            ],
            options={
                'db_table': 'data_unite',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='wilaya',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib_wilaya', models.CharField(db_column='lib_wilaya', max_length=120)),
                ('date_joined', models.DateTimeField(auto_now_add=True, db_column='date_joined', verbose_name='date joined')),
            ],
            options={
                'db_table': 'data_wilaya',
                'managed': False,
            },
        ),
    ]
