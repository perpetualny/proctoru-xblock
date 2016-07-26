# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProctorUExam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(verbose_name='heure de d&eacute;part')),
                ('actual_start_time', models.DateTimeField(null=True, verbose_name='Heure de d&eacute;but r&eacute;elle', blank=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_started', models.BooleanField(default=False)),
                ('is_canceled', models.BooleanField(default=False)),
                ('block_id', models.CharField(max_length=200)),
                ('end_time', models.DateTimeField(null=True, verbose_name='heure de fin', blank=True)),
                ('reservation_id', models.CharField(max_length=50)),
                ('reservation_no', models.CharField(max_length=200)),
                ('url', models.TextField()),
                ('user', models.ForeignKey(related_name='proctoru_exams', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProctoruUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(blank=True, max_length=100, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15} |  \\(\\d{3}\\)[-]\\d{3}[-\\.]??\\d{4}$ | \\d{3}[-]\\d{3}[-\\.]??\\d{4}$', message='Num&eacute;ro de t&eacute;l&eacute;phone doit &ecirc;tre saisi dans le format: &apos;999999999&apos;. Jusqu&apos;&agrave; 15 chiffres autoris&eacute;s.')])),
                ('time_zone', models.CharField(max_length=100)),
                ('time_zone_display_name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(related_name='proctoru_user', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='proctoruexam',
            unique_together=set([('user', 'block_id')]),
        ),
    ]
