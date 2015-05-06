# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salaries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='photo',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
