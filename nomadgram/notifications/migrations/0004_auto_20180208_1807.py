# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-08 09:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_notifications_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notifications',
            options={'ordering': ['-created_at']},
        ),
    ]
