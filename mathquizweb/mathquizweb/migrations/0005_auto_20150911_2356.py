# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mathquizweb', '0004_userquestiontypeoptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False),
        ),
        migrations.AlterField(
            model_name='questionstate',
            name='name',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='questiontype',
            name='name',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='userquestiontypeoptions',
            unique_together=set([('user', 'question_type')]),
        ),
    ]
