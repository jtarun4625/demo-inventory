# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 17:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0015_auto_20161228_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='product',
            field=models.ForeignKey(db_column='name', default='Gel(40gm)', on_delete=django.db.models.deletion.CASCADE, related_name='product_name', to='Inventory.Product'),
            preserve_default=False,
        ),
    ]
