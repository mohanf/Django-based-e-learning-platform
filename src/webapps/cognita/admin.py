# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from cognita.models import *


# Register your models here.

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lecture)
admin.site.register(Part)
admin.site.register(Reading)
admin.site.register(Video)
admin.site.register(Quiz)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(MCQuestion)
admin.site.register(BFQuestion)
admin.site.register(Choice)
admin.site.register(UserProgressCourse)
admin.site.register(UserProgressModule)
admin.site.register(UserAnswer)
admin.site.register(Grade)
admin.site.register(UserProfile)
admin.site.register(UserAnswerUnsubmit)
admin.site.register(StudentNote)
admin.site.register(Tag)


