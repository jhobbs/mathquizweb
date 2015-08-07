# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathquizweb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questiontype',
            old_name='users',
            new_name='blacklisted_users',
        ),
    ]
