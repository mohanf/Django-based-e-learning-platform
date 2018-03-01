# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import Module, Lecture

from django.shortcuts import render

# Create your views here.
def get_try(request):
    modules = Module.objects.all()
    context = {}
    index_l = 0
    index_t = 0
    module_list = []
    for module in modules:
        if module.module_type == 'L':
            index_l += 1
            newpair = [module, index_l]
            module_list.append(newpair)
        else:
            index_t += 1
            newpair = [module, index_t]
            module_list.append(newpair)
    context['module_list'] = module_list
    #yu = Lecture.objects.get(id=3)
    #print yu.expected_hour
    ui = Lecture.objects.filter(id=2)
    print ui
    return render(request, 'try.html', context)
