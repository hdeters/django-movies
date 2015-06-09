# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('rating', models.IntegerField()),
            ],
        ),
        migrations.RenameModel(
            old_name='Movies',
            new_name='Movie',
        ),
        migrations.RemoveField(
            model_name='ratings',
            name='movieid',
        ),
        migrations.RemoveField(
            model_name='ratings',
            name='userid',
        ),
        migrations.DeleteModel(
            name='Ratings',
        ),
        migrations.AddField(
            model_name='rating',
            name='movieid',
            field=models.ForeignKey(to='ratings.Movie'),
        ),
        migrations.AddField(
            model_name='rating',
            name='userid',
            field=models.ForeignKey(to='ratings.Rater'),
        ),
    ]
