# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0002_auto_20150609_1804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='movieid',
        ),
        migrations.RemoveField(
            model_name='rater',
            name='userid',
        ),
    ]
