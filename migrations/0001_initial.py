# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Govt',
            fields=[
                ('name', models.CharField(max_length=60, serialize=False, primary_key=True)),
                ('full_name', models.CharField(max_length=60)),
                ('type', models.CharField(max_length=60)),
                ('population', models.IntegerField(null=True, blank=True)),
                ('viewable', models.NullBooleanField()),
                ('payroll_count', models.IntegerField(null=True, blank=True)),
                ('payroll_sum', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('ft_median', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('ft_avg', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('ft_max', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('text', models.TextField(null=True, blank=True)),
                ('url', models.CharField(max_length=200, null=True, blank=True)),
                ('pic', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'salaries_govts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last', models.CharField(max_length=60)),
                ('rest', models.CharField(max_length=60)),
                ('fullname', models.CharField(max_length=100)),
                ('dob', models.CharField(max_length=10, null=True, blank=True)),
                ('dept', models.CharField(max_length=60)),
                ('job', models.CharField(max_length=60)),
                ('status', models.CharField(max_length=30, null=True, blank=True)),
                ('hiredate', models.CharField(max_length=10, null=True, blank=True)),
                ('salary', models.DecimalField(null=True, max_digits=12, decimal_places=2)),
                ('display_sal', models.DecimalField(null=True, max_digits=12, decimal_places=2)),
                ('deferred', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('total_gross', models.DecimalField(null=True, max_digits=12, decimal_places=2)),
                ('extra', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('additional', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('masters', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('nameslug', models.CharField(max_length=60)),
                ('deptslug', models.CharField(max_length=60)),
                ('govslug', models.CharField(max_length=60)),
                ('year', models.IntegerField(max_length=4)),
                ('comments', models.TextField(blank=True)),
                ('length', models.IntegerField(max_length=3, null=True, blank=True)),
                ('bigwig', models.CharField(max_length=50, null=True, blank=True)),
                ('govt', models.ForeignKey(to='salaries.Govt')),
            ],
            options={
                'db_table': 'salaries',
            },
            bases=(models.Model,),
        ),
    ]
