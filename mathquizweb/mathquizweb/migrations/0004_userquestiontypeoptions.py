# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mathquizweb', '0003_auto_20150815_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserQuestionTypeOptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('options', models.TextField()),
                ('question_type', models.ForeignKey(to='mathquizweb.QuestionType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
