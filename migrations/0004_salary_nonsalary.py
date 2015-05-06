# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salaries', '0003_salary_bonus_allowances'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='nonsalary',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
