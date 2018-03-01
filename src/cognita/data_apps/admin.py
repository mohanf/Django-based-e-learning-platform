# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from data_apps.models import Lecture, Test, Module, Course, Quiz, Reading, Part


# Register your models here.
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lecture)
admin.site.register(Test)
admin.site.register(Quiz)
admin.site.register(Reading)
admin.site.register(Part)