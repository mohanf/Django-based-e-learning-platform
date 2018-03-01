# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from cognita.forms_mohanf import CourseForm, LectureForm, ReadingForm, VideoForm, DeletePartForm, DeleteModuleForm, SearchOptionForm, UpperReadingForm, MaterialForm, LowerReadingForm, TagForm, DeleteTagForm
from django.http import HttpResponse, Http404
from cognita.models import Course, Module, Lecture, Part, Reading, Video, Quiz, Tag
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from mimetypes import guess_type
from django.contrib import messages
import operator
from django.db.models import Q, Count
import json


# Create your views here.


@login_required
def add_course(request):
    context = {}
    if request.method == 'GET':
        form = CourseForm()
        context['form'] = form
        return render(request, 'cognita/creator/add_course.html', context)
    form = CourseForm(request.POST, request.FILES)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'cognita/creator/add_course.html', context)
    new_course = form.save(commit=False)
    new_course.creator = request.user
    new_course.save()
    #print new_course.id
    return redirect(reverse('creating_course', kwargs={'course_id': new_course.id}))


@login_required
def creating_course(request, course_id):
    context = {}
    course = get_object_or_404(Course, id=course_id)
    if request.user != course.creator or course.published:
        raise Http404('Page not found')
    context['course'] = course
    modules = course.module_set.all()
    lecture_ind = 0
    test_ind = 0
    module_list = []
    for module in modules:
        if module.module_type == 'L':
            lecture_ind += 1
            module_list.append([module, lecture_ind])
        else:
            test_ind += 1
            module_list.append([module, test_ind])
    context['module_list'] = module_list
    lecture_form = LectureForm()
    context['lecture_form'] = lecture_form
    reading_form = ReadingForm()
    video_form = VideoForm()
    material_form = UpperReadingForm()
    context['reading_form'] = reading_form
    context['video_form'] = video_form
    context['material_form'] = material_form
    return render(request, 'cognita/creator/creating_course.html', context)


@login_required
def add_lecture(request, course_id):
    if request.method == 'GET':
        return render(request, 'cognita/creator/success.json')
    course = get_object_or_404(Course, id=course_id)
    if request.user != course.creator or course.published:
        raise Http404('Page not found')
    lecture_form = LectureForm(request.POST)
    if not lecture_form.is_valid():
        return HttpResponse(lecture_form.errors.as_json(), content_type='application/json')
    new_lecture = lecture_form.save(commit=False)
    new_lecture.module_type = 'L'
    new_lecture.course = course
    new_lecture.expected_hour = 0
    prenum = course.module_set.count()
    new_lecture.index = prenum + 1
    new_lecture.save()
    return render(request, 'cognita/creator/success.json')


@login_required
def add_reading(request, lecture_id):
    context = {}
    lecture = get_object_or_404(Lecture, id=lecture_id)
    course = lecture.course
    if request.method == 'GET':
        return redirect(reverse('creating_course', kwargs={'course_id': course.id}))
    print request.POST

    course = lecture.course
    if request.user != course.creator or course.published:
        raise Http404('Page not found')
    reading_form = ReadingForm(request.POST, request.FILES)
    if not reading_form.is_valid():
        #print 'aaa'
        #print reading_form.errors
        return HttpResponse(reading_form.errors.as_json(), content_type='application/json')
    new_reading = reading_form.save(commit=False)
    new_reading.part_type = 'R'
    new_reading.lecture = lecture
    cur = lecture.expected_hour
    lecture.expected_hour = cur + new_reading.expected_hour
    lecture.save()
    prenum = lecture.part_set.count()
    new_reading.index = prenum + 1
    #print prenum
    new_reading.save()
    part_context = {}
    part_context['part'] = get_object_or_404(Part, id=new_reading.id)


    part_html = render_to_string('cognita/creator/part.html', part_context).replace('\n', '')
    context['part_html'] = part_html
    
    context['panel_id'] = lecture.id
    return render(request, 'cognita/creator/success_part.json', context)


@login_required
def add_material(request, lecture_id):
    context = {}
    lecture = get_object_or_404(Lecture, id=lecture_id)
    course = lecture.course
    if request.method == 'GET':
        return redirect(reverse('creating_course', kwargs={'course_id': course.id}))
    if request.user != course.creator or course.published:
        raise Http404('Page not found')
    material_form = UpperReadingForm(request.POST)
    if not material_form.is_valid():
        return HttpResponse(material_form.errors.as_json(), content_type='application/json')
    new_material = material_form.save(commit=False)
    new_material.part_type = 'R'
    new_material.reading_type = 'M'
    new_material.lecture = lecture
    cur = lecture.expected_hour
    lecture.expected_hour = cur + new_material.expected_hour
    lecture.save()
    prenum = lecture.part_set.count()
    new_material.index = prenum + 1
    new_material.save()
    context['part_id'] = new_material.id
    return render(request, 'cognita/creator/success_material.json', context)


@login_required
def add_video(request, lecture_id):
    context = {}
    if request.method == 'GET':
        return redirect(reverse('creating_course'))
    lecture = get_object_or_404(Lecture, id=lecture_id)
    course = lecture.course
    if request.user != course.creator or course.published:
        raise Http404('Page not found')
    video_form = VideoForm(request.POST)
    if not video_form.is_valid():
        return HttpResponse(video_form.errors.as_json(), content_type='application/json')
    new_video = video_form.save(commit=False)
    new_video.part_type = 'V'
    new_video.lecture = lecture
    cur = lecture.expected_hour
    lecture.expected_hour = cur + new_video.expected_hour
    lecture.save()
    prenum = lecture.part_set.count()
    new_video.index = prenum + 1
    new_video.save()
    part_context = {}
    part_context['part'] = get_object_or_404(Part, id=new_video.id)
    part_html = render_to_string('cognita/creator/part.html', part_context).replace('\n', '')
    context['part_html'] = part_html
    context['panel_id'] = lecture.id
    return render(request, 'cognita/creator/success_part.json', context)


@login_required
def modify_course(request, course_id):
    context = {}
    course = get_object_or_404(Course, id=course_id)
    if course.creator != request.user or course.published:
        raise Http404('Page not found')
    if request.method == 'GET':
        course_form = CourseForm(instance=course)
        context['course'] = course
        context['form'] = course_form
        return render(request, 'cognita/creator/view_course_info.html', context)
    course_form = CourseForm(request.POST, request.FILES, instance=course)
    if not course_form.is_valid():
        context['form'] = course_form
        context['course'] = course
        return render(request, 'cognita/creator/view_course_info.html', context)
    course_form.save()
    return redirect(reverse('creating_course', kwargs={'course_id': course.id}))


@login_required
def modify_lecture(request, lecture_id):
    context = {}
    lecture = get_object_or_404(Lecture, id=lecture_id)

    if lecture.course.creator != request.user or lecture.course.published:
        raise Http404('Page not found')
    if request.method == 'GET':
        lecture_form = LectureForm(instance=lecture)
        context['lecture'] = lecture
        context['form'] = lecture_form
        return render(request, 'cognita/creator/view_lecture_info.html', context)
    lecture_form = LectureForm(request.POST, instance=lecture)
    if not lecture_form.is_valid():
        context['form'] = lecture_form
        context['lecture'] = lecture
        return render(request, 'cognita/creator/view_lecture_info.html', context)
    lecture_form.save()
    return redirect(reverse('creating_course', kwargs={'course_id': lecture.course.id}))


@login_required
def view_part(request, part_id):
    context = {}
    part = get_object_or_404(Part, id=part_id)
    if part.lecture.course.creator != request.user or part.lecture.course.published:
        raise Http404('Page not found')
    if part.part_type == 'R':
        reading = part.reading
        context['reading'] = reading
        context['mode'] = 'view'
        if reading.reading_type == 'P':
            form = ReadingForm(instance=reading)
            context['form'] = form
            return render(request, 'cognita/creator/view_reading.html', context)
        else:
            form = MaterialForm(instance=reading)
            context['form'] = form
            return render(request, 'cognita/creator/view_material.html', context)

    if part.part_type == 'V':
        video = part.video
        context['mode'] = 'view'
        form = VideoForm(instance=video)
        context['form'] = form
        context['video'] = video
        return render(request, 'cognita/creator/view_video.html', context)


@login_required
def start_material(request, reading_id):
    reading = get_object_or_404(Reading, id=reading_id)
    if reading.lecture.course.creator != request.user or reading.lecture.course.published:
        raise Http404('Page not found')
    context = {}
    context['reading'] = reading
    context['mode'] = 'modify'
    if reading.reading_type == 'P':
        return redirect(reverse('creating_course', kwargs={'course_id': reading.lecture.course.id}))
    form = MaterialForm(instance=reading)
    context['form'] = form
    return render(request, 'cognita/creator/view_material.html', context)


@login_required
def get_reading(request, reading_id):
    reading = get_object_or_404(Reading, id=reading_id)
    if reading.lecture.course.creator != request.user or reading.lecture.course.published:
        raise Http404
    if not reading.file:
        raise Http404

    content_type = 'application/pdf'
    response = HttpResponse(reading.file, content_type=content_type)
    response['Content-Disposition'] = 'inline'
    return response


@login_required()
def modify_reading(request, reading_id):
    context = {}
    reading = get_object_or_404(Reading, id=reading_id)
    if reading.reading_type == 'M':
        return redirect(reverse('creating_course', kwargs={'course_id': reading.lecture.course.id}))
    if reading.lecture.course.creator != request.user or reading.lecture.course.published:
        raise Http404
    if request.method == 'GET':
        return redirect(reverse('view_part', kwargs={'part_id': reading.id}))
    reading_form = ReadingForm(request.POST, request.FILES, instance=reading)
    if not reading_form.is_valid():
        context['form'] = reading_form
        context['mode'] = 'modify'
        context['reading'] = reading
        return render(request, 'cognita/creator/view_reading.html', context)
    reading_form.save()

    return redirect(reverse('creating_course', kwargs={'course_id': reading.lecture.course.id}))


@login_required
def modify_material(request, reading_id):
    context = {}
    reading = get_object_or_404(Reading, id=reading_id)
    if reading.reading_type == 'P':
        return redirect(reverse('creating_course', kwargs={'course_id': reading.lecture.course.id}))
    if reading.lecture.course.creator != request.user or reading.lecture.course.published:
        raise Http404
    if request.method == 'GET':
        return redirect(reverse('view_part', kwargs={'part_id': reading.id}))
    material_form = MaterialForm(request.POST, instance=reading)
    if not material_form.is_valid():
        context['form'] = material_form
        context['mode'] = 'modify'
        context['reading'] = reading
        return render(request, 'cognita/creator/view_material.html', context)
    material_form.save()

    return redirect(reverse('view_part', kwargs={'part_id': reading.id}))


@login_required
def modify_video(request, video_id):
    context = {}
    video = get_object_or_404(Video, id=video_id)
    if video.lecture.course.creator != request.user or video.lecture.course.published:
        raise Http404
    if request.method == 'GET':
        return redirect(reverse('view_part', kwargs={'part_id': video.id}))
    video_form = VideoForm(request.POST, instance=video)
    if not video_form.is_valid():
        context['form'] = video_form
        context['mode'] = 'modify'
        context['video'] = video
        return render(request, 'cognita/creator/view_video.html', context)
    video_form.save()
    return redirect(reverse('creating_course', kwargs={'course_id': video.lecture.course.id}))


@login_required()
def delete_part(request):
    if request.method == 'GET':
        raise Http404
    delete_form = DeletePartForm(request.POST)
    if not delete_form.is_valid():
        raise Http404
    part_id = delete_form.cleaned_data['part_id']
    part = get_object_or_404(Part, id=part_id)
    lecture = part.lecture
    if lecture.course.creator != request.user or lecture.course.published:
        raise Http404
    this_index = part.index
    target_parts = Part.objects.filter(lecture=lecture, index__gt=this_index)
    for target_part in target_parts:
        target_part.index = target_part.index - 1
        target_part.save()
    tot_hours = lecture.expected_hour
    lecture.expected_hour = tot_hours - part.expected_hour
    lecture.save()
    part.delete()
    return render(request, 'cognita/creator/success.json')


@login_required()
def delete_module(request):
    if request.method == 'GET':
        raise Http404
    delete_form = DeleteModuleForm(request.POST)
    if not delete_form.is_valid():
        raise Http404
    module_id = delete_form.cleaned_data['module_id']
    module = get_object_or_404(Module, id=module_id)
    course = module.course
    if course.creator != request.user or course.published:
        raise Http404
    this_index = module.index
    target_modules = Module.objects.filter(course=course, index__gt=this_index)
    for target_module in target_modules:
        target_module.index = target_module.index - 1
        target_module.save()
    module.delete()
    return render(request, 'cognita/creator/success.json')


@login_required
def publish(request, course_id):
    if request.method == 'GET':
        raise Http404
    course = get_object_or_404(Course, id=course_id)
    if course.creator != request.user or course.published:
        raise Http404
    modules = course.module_set.all()
    publish_flag = 1
    for module in modules:
        if module.module_type == 'L':
            num_part = module.lecture.part_set.all().count()
            if not num_part:
                publish_flag = 0
                messages.add_message(request, messages.INFO, 'You could not leave lectures blank!\n')
            quizes = Quiz.objects.filter(lecture=module.lecture)
            for quiz in quizes:
                num_question = quiz.questions.all().count()
                if not num_question:
                    publish_flag = 0
                    messages.add_message(request, messages.INFO, 'You could not leave quizes blank!\n')

        else:
            num_question = module.test.questions.all().count()
            if not num_question:
                publish_flag = 0
                messages.add_message(request, messages.INFO, 'You could not leave tests blank!\n')

    if publish_flag:
        course.published = True
        course.save()
        return redirect(reverse('self_profile'))
    return redirect(reverse('creating_course', kwargs={'course_id': course_id}))


@login_required
def reorder_part(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    course = lecture.course
    if course.creator != request.user or course.published:
        raise Http404
    if request.method == 'GET':
        return redirect(reverse('creating_course', kwargs={'course_id': course.id}))
    part_id_list = request.POST.getlist('part[]')
    #print request.POST
    part_list = []
    if len(part_id_list) != lecture.part_set.count() or len(part_id_list) != len(set(part_id_list)):
        raise Http404
    for part_id in part_id_list:
        part = get_object_or_404(Part, id=part_id)
        if part.lecture != lecture:
            raise Http404
        part_list.append(part)
    counter = 0
    for part in part_list:
        counter += 1
        part.index = counter
        part.save()
    return render(request, 'cognita/creator/success.json')


@login_required
def reorder_module(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.creator != request.user or course.published:
        raise Http404
    if request.method == 'GET':
        return redirect(reverse('creating_course', kwargs={'course_id': course.id}))
    module_id_list = request.POST.getlist('module[]')
    module_list = []
    if len(module_id_list) != course.module_set.count() or len(module_id_list) != len(set(module_id_list)):
        raise Http404
    for module_id in module_id_list:
        module = get_object_or_404(Module, id=module_id)
        if module.course != course:
            raise Http404
        module_list.append(module)
    counter = 0
    for module in module_list:
        counter += 1
        module.index = counter
        module.save()
    return render(request, 'cognita/creator/success.json')


def search(request):
    context = {}
    input_sort = {'sort_by': 'P'}
    context['form1'] = SearchOptionForm(input_sort)
    print 'aaa'
    if 'srch-term' in request.GET:
        to_be_searched = request.GET['srch-term'].strip()
        # print 'bbb'
        # print len(to_be_searched)
        input_sort['srch_term'] = to_be_searched
        context['form1'] = SearchOptionForm(input_sort)
        if not len(to_be_searched):
            return render(request, 'cognita/creator/search_result.html', context)
        to_be_searched.replace('+', ' ')
        word_list = to_be_searched.split()
        print word_list
        query = reduce(operator.and_, ((Q(title__icontains = item) | Q(description__icontains = item) | Q(tags__tag_content__icontains = item)) for item in word_list))
        course_list = Course.objects.filter(published=True).filter(query).distinct().annotate(s_count = Count('students')).order_by('-s_count')
        context['course_list'] = course_list
        print course_list
    return render(request, 'cognita/creator/search_result.html', context)


def search_with_option(request):
    context_json = {}
    context_html = {}
    form = SearchOptionForm(request.GET)
    if not form.is_valid():
        #print form.errors
        raise Http404
    to_be_searched = form.cleaned_data['srch_term']
    if not len(to_be_searched):
        raise Http404
    to_be_searched.replace('+', ' ')
    word_list = to_be_searched.split()
    query1 = reduce(operator.and_, ((Q(title__icontains=item) | Q(description__icontains=item) | Q(tags__tag_content__icontains = item)) for item in word_list))
    if form.cleaned_data.get('filter_with', ''):
        filter_list = form.cleaned_data['filter_with']
        query2 = reduce(operator.or_, (Q(category__exact = item) for item in filter_list))
        course_list = Course.objects.filter(published=True).filter(query1).filter(query2).distinct().annotate(s_count = Count('students')).order_by('-s_count')
    else:
        #print 'ccc'
        course_list = Course.objects.filter(published=True).filter(query1).distinct().annotate(s_count = Count('students')).order_by('-s_count')

    if form.cleaned_data.get('sort_by', '') == 'C':
        #print 'bbb'
        course_list = course_list.order_by('-created_at')
        # else:
        # course_list = course_list.order_by('-s_count')
    context_html['course_list'] = course_list
    context_html['request'] = request
    html = render_to_string('cognita/creator/course_search.html', context_html)
    context_json['course_list_html'] = html
    return render(request, 'cognita/creator/success_search.json', context_json)


@login_required
def save_material(request, reading_id):
    context = {}
    reading = get_object_or_404(Reading, id=reading_id)
    #print request.POST
    if reading.reading_type == 'P':
        return redirect(reverse('creating_course', kwargs={'course_id': reading.lecture.course.id}))
    if reading.lecture.course.creator != request.user or reading.lecture.course.published:
        raise Http404
    if request.method == 'GET':
        return redirect(reverse('view_part', kwargs={'part_id': reading.id}))
    material_form = LowerReadingForm(request.POST, instance=reading)
    if not material_form.is_valid():
        return HttpResponse(material_form.errors.as_json(), content_type='application/json')
    material = material_form.save()

    return render(request, 'cognita/creator/success.json')


@login_required
def add_tag(request, course_id):
    context_html = {}
    context_json = {}
    course = get_object_or_404(Course, id=course_id)
    if course.creator != request.user or course.published:
        raise Http404
    form = TagForm(request.POST)
    if not form.is_valid():
        return HttpResponse(form.errors.as_json(), content_type='application/json')
    tag_content = form.cleaned_data.get('tag_content')
    tag, created = Tag.objects.get_or_create(tag_content=tag_content)
    course.tags.add(tag)
    course.save()
    context_html['tag'] = tag
    new_html = render_to_string('cognita/creator/single_tag.html', context_html)
    context_json['tag_html'] = new_html
    return render(request, 'cognita/creator/success_tag.json', context_json)


def complete(request):
    #print 'aaa'
    if 'term' not in request.GET:
        raise Http404
    #print request.GET
    keyword = request.GET['term']
    tag_list = Tag.objects.filter(tag_content__icontains=keyword).order_by('tag_content')
    results = []
    count = 0
    for tag in tag_list:
        if count >= 10:
            break
        count += 1
        tag_json = {}
        tag_json['id'] = tag.id
        tag_json['label'] = tag.tag_content
        tag_json['value'] = tag.tag_content
        results.append(tag_json)
    data = json.dumps(results)
    return HttpResponse(data, content_type="application/json")


@login_required
def delete_tag(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.creator != request.user or course.published:
        #print 'aaa'
        raise Http404
    form = DeleteTagForm(request.POST)
    if not form.is_valid():
        return HttpResponse(form.errors.as_json(), content_type='application/json')
    tag_id = form.cleaned_data['tag_id']
    tag = Tag.objects.get(id=tag_id)
    course.tags.remove(tag)
    course.save()
    if not tag.tagged_course.count():
        tag.delete()
    return render(request, 'cognita/creator/success.json')
