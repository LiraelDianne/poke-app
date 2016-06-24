# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 20:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poke_app', '0004_auto_20160624_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poke',
            name='pokes',
        ),
        migrations.AlterField(
            model_name='poke',
            name='poked',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poked_set', to='poke_app.User'),
        ),
        migrations.AlterField(
            model_name='poke',
            name='poker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poke_set', to='poke_app.User'),
        ),
    ]
