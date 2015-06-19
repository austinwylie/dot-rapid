# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rapid', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datalayer',
            name='bbox',
        ),
        migrations.AddField(
            model_name='feature',
            name='hash',
            field=models.TextField(unique=True, null=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apitoken',
            name='key',
            field=models.TextField(unique=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='datalayer',
            name='uid',
            field=models.TextField(unique=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='datasource',
            name='url',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feature',
            name='create_timestamp',
            field=models.TimeField(db_index=True, auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feature',
            name='uid',
            field=models.TextField(unique=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geoview',
            name='uid',
            field=models.TextField(unique=True, db_index=True),
            preserve_default=True,
        ),
    ]
