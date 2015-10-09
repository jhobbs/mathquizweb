# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathquizweb', '0005_auto_20150911_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answered_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
