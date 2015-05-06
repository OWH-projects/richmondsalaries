# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salaries', '0002_salary_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='bonus_allowances',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
