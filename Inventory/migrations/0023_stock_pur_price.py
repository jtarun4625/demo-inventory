# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-02 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0022_stock_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='pur_price',
            field=models.IntegerField(default=0),
        ),
    ]
