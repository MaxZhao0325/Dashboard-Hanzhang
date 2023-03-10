# Generated by Django 3.2.4 on 2021-06-18 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmaStoringData',
            fields=[
                ('time', models.DateTimeField()),
                ('event_vct', models.CharField(blank=True, max_length=100, null=True)),
                ('stats_vct', models.CharField(blank=True, max_length=100, null=True)),
                ('action', models.IntegerField(blank=True, null=True)),
                ('reward', models.FloatField(blank=True, null=True)),
                ('action_vct', models.CharField(blank=True, max_length=100, null=True)),
                ('message_name', models.CharField(blank=True, max_length=100, null=True)),
                ('uploaded', models.IntegerField(blank=True, null=True)),
                ('dep_id', models.IntegerField()),
                ('p_key', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'ema_storing_data',
                'managed': False,
            },
        ),
    ]
