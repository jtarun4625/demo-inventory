# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-01 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0018_remove_purchase_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.Product')),
                ('stock', models.ForeignKey(db_column='stock', on_delete=django.db.models.deletion.CASCADE, related_name='stocksGet', to='Inventory.Purchase')),
            ],
        ),
    ]