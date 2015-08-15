# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mathquizweb', '0002_auto_20150807_0408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questiontype',
            name='blacklisted_users',
        ),
        migrations.AddField(
            model_name='questiontype',
            name='enabled_users',
            field=models.ManyToManyField(related_name='enabled_questions', to=settings.AUTH_USER_MODEL),
        ),
    ]
