# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathquizweb', '0003_auto_20150815_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answered_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
