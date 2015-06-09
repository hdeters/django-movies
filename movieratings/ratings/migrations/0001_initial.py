# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('movieid', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('genres', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Rater',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('userid', models.IntegerField()),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=1)),
                ('occupation', models.IntegerField()),
                ('zipcode', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('rating', models.IntegerField()),
                ('movieid', models.ForeignKey(to='ratings.Movies')),
                ('userid', models.ForeignKey(to='ratings.Rater')),
            ],
        ),
    ]
