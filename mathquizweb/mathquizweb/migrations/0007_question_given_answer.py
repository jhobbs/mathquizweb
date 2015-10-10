# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathquizweb', '0006_question_answered_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='given_answer',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
