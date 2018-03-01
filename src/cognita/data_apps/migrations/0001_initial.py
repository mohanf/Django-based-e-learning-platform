# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-24 05:12
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.BooleanField(default=False)),
                ('creator_info', models.TextField()),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('CS', 'Computer Science'), ('MATH', 'Mathematics'), ('ART', 'Art'), ('BUS', 'Business'), ('SCI', 'Natural Science'), ('SSCI', 'Social Science'), ('LIT', 'Literature'), ('UCL', 'Unclassified')], default='UCL', max_length=5)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(related_name='r_course', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_type', models.CharField(choices=[('L', 'Lecture'), ('T', 'Test')], default='L', max_length=1)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('index', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('index', models.PositiveIntegerField()),
                ('expected_hour', models.FloatField()),
                ('part_type', models.CharField(choices=[('R', 'Reading'), ('V', 'Video')], default='R', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField()),
                ('weight', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('description', models.TextField(max_length=40000)),
                ('image', models.ImageField(blank=True, null=True, upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=40000)),
                ('full_score', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('MC', 'Multiple Choice'), ('SR', 'Short Answer')], max_length=2)),
                ('answer', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProgressPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserProgressTotal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_apps.Course')),
            ],
        ),
        migrations.CreateModel(
            name='BFQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data_apps.Question')),
                ('answer', models.CharField(max_length=255)),
            ],
            bases=('data_apps.question',),
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('module_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data_apps.Module')),
                ('expected_hour', models.FloatField(blank=True, null=True)),
            ],
            bases=('data_apps.module',),
        ),
        migrations.CreateModel(
            name='MCQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data_apps.Question')),
            ],
            bases=('data_apps.question',),
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('part_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data_apps.Part')),
                ('file', models.FileField(upload_to='readings')),
            ],
            bases=('data_apps.part',),
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('module_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data_apps.Module')),
                ('full_score', models.PositiveIntegerField()),
            ],
            bases=('data_apps.module',),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('part_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data_apps.Part')),
                ('link', models.TextField()),
            ],
            bases=('data_apps.part',),
        ),
        migrations.AddField(
            model_name='userprogresstotal',
            name='module_completed',
            field=models.ManyToManyField(related_name='r_module', to='data_apps.Module'),
        ),
        migrations.AddField(
            model_name='userprogresstotal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprogresspart',
            name='partProgress',
            field=models.ManyToManyField(related_name='r_part', to='data_apps.Part'),
        ),
        migrations.AddField(
            model_name='userprogresspart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='useranswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_apps.Question'),
        ),
        migrations.AddField(
            model_name='useranswer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data_apps.Quiz'),
        ),
        migrations.AddField(
            model_name='module',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_apps.Course'),
        ),
        migrations.AddField(
            model_name='grade',
            name='quiz',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='data_apps.Quiz'),
        ),
        migrations.AddField(
            model_name='grade',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprogresspart',
            name='lecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_apps.Lecture'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='lecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_apps.Lecture'),
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data_apps.Test'),
        ),
        migrations.AddField(
            model_name='part',
            name='lecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_apps.Lecture'),
        ),
        migrations.AddField(
            model_name='grade',
            name='test',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='data_apps.Test'),
        ),
        migrations.AddField(
            model_name='choices',
            name='mcquestion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_apps.MCQuestion'),
        ),
    ]