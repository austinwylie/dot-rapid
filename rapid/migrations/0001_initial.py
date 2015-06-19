# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiCall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('call', models.TextField()),
                ('timestamp', models.TimeField(auto_now_add=True, null=True)),
                ('ip', models.TextField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApiToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.TextField(unique=True)),
                ('descriptor', models.TextField(unique=True)),
                ('issued', models.TimeField(auto_now_add=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.TextField()),
                ('content', models.TextField(null=True)),
                ('internet_media_type', models.TextField(null=True)),
                ('create_timestamp', models.TimeField(auto_now_add=True, null=True)),
                ('export_original_file', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataLayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.TextField()),
                ('descriptor', models.TextField()),
                ('bbox', django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True)),
                ('is_public', models.BooleanField(default=False)),
                ('properties', models.TextField(null=True)),
                ('include_features', models.NullBooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataLayerRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.IntegerField(default=0)),
                ('layer', models.ForeignKey(to='rapid.DataLayer')),
                ('token', models.ForeignKey(to='rapid.ApiToken')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField()),
                ('update_interval', models.TimeField(null=True)),
                ('expected_type', models.TextField(null=True)),
                ('properties', models.TextField(null=True)),
                ('layer', models.ForeignKey(to='rapid.DataLayer', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.TextField()),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True)),
                ('bbox', django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True)),
                ('properties', models.TextField(null=True)),
                ('create_timestamp', models.TimeField(auto_now_add=True, null=True)),
                ('modified_timestamp', models.TimeField(auto_now=True, null=True)),
                ('archive', models.ForeignKey(to='rapid.Archive', null=True)),
                ('layer', models.ForeignKey(to='rapid.DataLayer', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GeoView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.TextField()),
                ('descriptor', models.TextField()),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True)),
                ('bbox', django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True)),
                ('properties', models.TextField(null=True)),
                ('include_layers', models.NullBooleanField()),
                ('include_geom', models.NullBooleanField()),
                ('layers', models.ManyToManyField(to='rapid.DataLayer', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GeoViewRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.IntegerField(default=0)),
                ('geo_view', models.ForeignKey(to='rapid.GeoView')),
                ('token', models.ForeignKey(to='rapid.ApiToken')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='archive',
            name='layer',
            field=models.ForeignKey(to='rapid.DataLayer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='apicall',
            name='token',
            field=models.ForeignKey(to='rapid.ApiToken', null=True),
            preserve_default=True,
        ),
    ]
