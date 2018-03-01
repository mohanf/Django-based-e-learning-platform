# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division
import collections

import re
from mimetypes import guess_type

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from cognita.forms_xinyangg import *

@login_required
def create_test(request, course_id):
    context = {}
    course = get_object_or_404(Course, id=course_id)
    if request.user != course.creator:
        return redirect('creating_course', course_id=course_id)
    if course.published == True:
        return redirect('home')
    context['course'] = course
    if request.method == 'GET':
        form = TestForm()
        context['form'] = form
        return render(request, 'cognita/xinyangg/create_quiz_test.html', context)
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.module_type = 'T'
            test.course = course
            test.index = Module.objects.filter(course_id__exact=course_id).count() + 1
            test.save()
            return redirect('update_test', test_id=test.id)
        else:
            context['form'] = form
            return render(request, 'cognita/xinyangg/create_quiz_test.html', context)

@login_required
def create_quiz(request,lecture_id):
    context = {}
    lecture = get_object_or_404(Lecture, id=lecture_id)
    if request.user != lecture.course.creator:
        return redirect('creating_course', course_id=lecture.course_id)
    if lecture.course.published == True:
        return redirect('home')
    context['lecture'] = lecture
    context['course'] = lecture.course
    if request.method == 'GET':
        form = QuizForm()
        context['form'] = form
        return render(request, 'cognita/xinyangg/create_quiz_test.html', context)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.lecture = lecture
            quiz.index = Part.objects.filter(lecture_id__exact=lecture_id).count() + 1
            quiz.part_type = 'Q'
            quiz.save()
            lecture.expected_hour = lecture.expected_hour + quiz.expected_hour
            lecture.save()
            return redirect('update_quiz', quiz_id=quiz.id)
        else:
            context['form'] = form
            return render(request, 'cognita/xinyangg/create_quiz_test.html', context)

@login_required
def update_test(request, test_id):
    context = {}
    test = get_object_or_404(Test, id=test_id)
    if request.user != test.course.creator:
        return redirect('creating_course', course_id=test.course_id)
    if test.course.published == True:
        return redirect('home')
    context['course'] = test.course
    if request.method == 'GET':
        form = TestForm(instance=test)
        context['form'] = form
        context['questions'] = test.questions.all().order_by('index')
        return render(request, 'cognita/xinyangg/update_quiz_test.html', context)

@login_required
def update_test_info(request, test_id):
    context = {}
    test = get_object_or_404(Test, id=test_id)
    if request.user != test.course.creator:
        return redirect('creating_course', course_id=test.course_id)
    if test.course.published == True:
        return redirect('home')
    form = TestForm(request.POST, instance=test)
    if form.is_valid():
        form.save()
        context['form'] = form.cleaned_data
        context['success'] = True
        return JsonResponse(context)
    else:
        context['form'] ={}
        context['success'] = False
        context['error'] = {}
        for k, v in form.errors.items():
            context['error'][k] = v[0]
        if 'title' in context['error']:
            context['form']['title'] = test.title
        else:
            context['form']['title'] = form.cleaned_data['title']
        if 'description' in context['error']:
            context['form']['description'] = test.description
        else:
            context['form']['description'] = form.cleaned_data['description']
        if 'full_score' in context['error']:
            context['form']['full_score'] = test.full_score
        else:
            context['form']['full_score'] = form.cleaned_data['full_score']
        if 'expected_hour' in context['error']:
            context['form']['expected_hour'] = test.expected_hour
        else:
            context['form']['expected_hour'] = form.cleaned_data['expected_hour']
        return JsonResponse(context)

@login_required
def update_quiz(request, quiz_id):
    context = {}
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.user != quiz.lecture.course.creator:
        return redirect('creating_course', course_id=quiz.lecture.course_id)
    if quiz.lecture.course.published == True:
        return redirect('home')
    context['course'] = quiz.lecture.course
    context['lecture'] = quiz.lecture
    if request.method == 'GET':
        form = QuizForm(instance=quiz)
        context['questions'] = quiz.questions.all().order_by('index')
        context['form'] = form
        return render(request, 'cognita/xinyangg/update_quiz_test.html', context)

@login_required
def update_quiz_info(request, quiz_id):
    context = {}
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.user != quiz.lecture.course.creator:
        return redirect('creating_course', course_id=quiz.lecture.course_id)
    if quiz.lecture.course.published == True:
        return redirect('home')
    form = QuizForm(request.POST, instance=quiz)
    if form.is_valid():
        form.save()
        context['form'] = form.cleaned_data
        context['success'] = True
        return JsonResponse(context)
    else:
        context['form'] ={}
        context['success'] = False
        context['error'] = {}
        for k, v in form.errors.items():
            context['error'][k] = v[0]
        if 'title' in context['error']:
            context['form']['title'] = quiz.title
        else:
            context['form']['title'] = form.cleaned_data['title']
        if 'description' in context['error']:
            context['form']['description'] = quiz.description
        else:
            context['form']['description'] = form.cleaned_data['description']
        if 'full_score' in context['error']:
            context['form']['full_score'] = quiz.full_score
        else:
            context['form']['full_score'] = form.cleaned_data['full_score']
        if 'expected_hour' in context['error']:
            context['form']['expected_hour'] = quiz.expected_hour
        else:
            context['form']['expected_hour'] = form.cleaned_data['expected_hour']
        return JsonResponse(context)

@login_required
def create_question_test(request,test_id):
    test = get_object_or_404(Test, id=test_id)
    if request.user != test.course.creator:
        return redirect('creating_course', course_id=test.course_id)
    if test.course.published == True:
        return redirect('home')
    if request.method == 'GET':
        context = {}
        context['course'] = test.course
        context['test'] = test.title
        question_form = MCQuestionForm()
        context['question_form'] = question_form
        context['choice_forms'] = collections.OrderedDict()
        for i in range(3):
            context['choice_forms'][chr(65+i)] = ChoiceForm()
        context['all_correct_choice'] = []
        return render(request, 'cognita/xinyangg/create_question.html', context)
    if request.method == 'POST':
        context = {}
        context['course'] = test.course
        context['test'] = test.title
        if request.POST.get('question_type') == "MC":
            question_form = MCQuestionForm(request.POST, request.FILES)
            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.test = test
                question.index = Question.objects.filter(test_id__exact=test_id).count() + 1
                question.type = 'MC'
                question.save()
                context, valid = save_choice(request, question, question_form, context)
                if valid:
                    if request.POST.get('save', None):
                        return redirect('update_test', test_id=test.id)
                    else:
                        return redirect('create_question_test', test_id=test.id)
                else:
                    return render(request, 'cognita/xinyangg/create_question.html', context)
            else:
                context['choice_forms'] = collections.OrderedDict()
                for i in range(3):
                    context['choice_forms'][chr(65 + i)] = ChoiceForm()
                context['question_form'] = question_form
                return render(request, 'cognita/xinyangg/create_question.html', context)

        if request.POST.get('question_type') == "BF":
            question_form = BFQuestionForm(request.POST, request.FILES)
            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.test = test
                question.index = Question.objects.filter(test_id__exact=test_id).count() + 1
                question.type = 'BF'
                question.save()
                context, valid = save_answer(request, question, question_form, context)
                if valid:
                    if request.POST.get('save', None):
                        return redirect('update_test', test_id=test.id)
                    else:
                        return redirect('create_question_test', test_id=test.id)
                else:
                    return render(request, 'cognita/xinyangg/create_question.html', context)
            else:
                context['answer_forms'] = []
                context['answer_forms'].append(BFQuestionAnswerForm())
                context['question_form'] = question_form
                return render(request, 'cognita/xinyangg/create_question.html', context)

    return render(request, 'cognita/xinyangg/create_question.html', {})

@login_required
def save_choice(request, question, question_form, context):
    content_list = request.POST.getlist('content')
    correct_list_raw = request.POST.getlist('choice_correct')
    correct_list = []
    for i in range(len(content_list)):
        if str(chr(i + 65)) in correct_list_raw:
            correct_list.append(True)
        else:
            correct_list.append(False)
    content_choice_pairs = zip(content_list, correct_list)
    context['all_correct_choice'] = correct_list_raw
    data_dicts = [{'content': content, 'correct': correct} for content, correct in content_choice_pairs]
    context['choice_forms'] = collections.OrderedDict()
    all_choice_valid = True
    i = 0
    j = 0
    for data in data_dicts:
        choice_form = ChoiceForm(data)
        if choice_form.is_valid():
            choice = choice_form.save(commit=False)
            choice.mcquestion = question
            choice.save()
            if choice.correct == True:
                j = j + 1
        else:
            all_choice_valid = False
        context['choice_forms'][chr(65 + i)] = choice_form
        i = i + 1
    if all_choice_valid == False:
        context['question_form'] = question_form
        question.delete()
        return context, False
    elif i < 2:
        context['error_message'] = "Number of choice should be at least 2."
        context['question_form'] = question_form
        question.delete()
        for i in range(i, 3):
            context['choice_forms'][chr(65 + i)] = ChoiceForm()
        context['all_correct_choice'] = []
        return context, False
    elif j < 1:
        context['error_message'] = "Number of correct choice should be at least 1."
        context['question_form'] = question_form
        question.delete()
        context['all_correct_choice'] = []
        return context, False
    else:
        return context, True

@login_required
def save_answer(request, question, question_form, context):
    answer_list = request.POST.getlist('answer')
    data_dicts = [{'answer': answer} for answer in answer_list]
    context['answer_forms'] = []
    all_answer_valid = True
    i = 0
    for data in data_dicts:
        answer_form = BFQuestionAnswerForm(data)
        if answer_form.is_valid():
            correct_answer = answer_form.save(commit=False)
            correct_answer.bfquestion = question
            correct_answer.save()
        else:
            all_answer_valid = False
        context['answer_forms'].append(answer_form)
        i = i + 1
    if all_answer_valid == False:
        context['question_form'] = question_form
        question.delete()
        return context, False
    elif i < 1:
        context['error_message'] = "Number of correct answer should be at least 1."
        context['question_form'] = question_form
        question.delete()
        context['answer_forms'] = []
        context['answer_forms'].append(BFQuestionAnswerForm())
        return context, False
    else:
        return context, True

@login_required
def create_question_quiz(request,quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.user != quiz.lecture.course.creator:
        return redirect('creating_course', course_id=quiz.lecture.course_id)
    if quiz.lecture.course.published == True:
        return redirect('home')
    if request.method == 'GET':
        context = {}
        context['course'] = quiz.lecture.course
        context['lecture'] = quiz.lecture
        context['quiz'] = quiz
        question_form = MCQuestionForm()
        context['question_form'] = question_form
        context['choice_forms'] = collections.OrderedDict()
        for i in range(3):
            context['choice_forms'][chr(65+i)] = ChoiceForm()
        context['all_correct_choice'] = []
        return render(request, 'cognita/xinyangg/create_question.html', context)
    if request.method == 'POST':
        context = {}
        context['course'] = quiz.lecture.course
        context['lecture'] = quiz.lecture
        context['quiz'] = quiz
        if request.POST.get('question_type') == "MC":
            question_form = MCQuestionForm(request.POST, request.FILES)
            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.quiz = quiz
                question.index = Question.objects.filter(quiz_id__exact=quiz_id).count() + 1
                question.type = 'MC'
                question.save()
                context, valid = save_choice(request, question, question_form, context)
                if valid:
                    if request.POST.get('save', None):
                        return redirect('update_quiz', quiz_id=quiz.id)
                    else:
                        return redirect('create_question_quiz', quiz_id=quiz.id)
                else:
                    return render(request, 'cognita/xinyangg/create_question.html', context)
            else:
                context['choice_forms'] = collections.OrderedDict()
                for i in range(3):
                    context['choice_forms'][chr(65 + i)] = ChoiceForm()
                context['question_form'] = question_form
                return render(request, 'cognita/xinyangg/create_question.html', context)

        if request.POST.get('question_type') == "BF":
            question_form = BFQuestionForm(request.POST, request.FILES)
            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.quiz = quiz
                question.index = Question.objects.filter(quiz_id__exact=quiz_id).count() + 1
                question.type = 'BF'
                question.save()
                context, valid = save_answer(request, question, question_form, context)
                if valid:
                    if request.POST.get('save', None):
                        return redirect('update_quiz', quiz_id=quiz.id)
                    else:
                        return redirect('create_question_quiz', quiz_id=quiz.id)
                else:
                    return render(request, 'cognita/xinyangg/create_question.html', context)
            else:
                context['answer_forms'] = []
                context['answer_forms'].append(BFQuestionAnswerForm())
                context['question_form'] = question_form
                return render(request, 'cognita/xinyangg/create_question.html', context)
    return render(request, 'cognita/xinyangg/create_question.html', {})

@login_required
def delete_question(request):
    question_id = request.POST.get('question_id', None)
    question = get_object_or_404(Question, id=question_id)
    context = {}
    if question.test:
        if request.user == question.test.course.creator:
            question.delete()
            context['question_id'] = question_id
    elif question.quiz:
        if request.user == question.quiz.lecture.course.creator:
            question.delete()
            context['question_id'] = question_id
    return JsonResponse(context)

@login_required
def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    context = {}
    if question.test:
        if request.user != question.test.course.creator:
            return redirect('course_page', course_id=question.test.course_id)
        if question.test.course.published == True:
            return redirect('home')
    elif question.quiz:
        if request.user != question.quiz.lecture.course.creator:
            return redirect('course_page', course_id=question.quiz.lecture.course_id)
        if question.quiz.lecture.course.published == True:
            return redirect('home')
    if question.type == 'MC':
        if question.test:
            context['course'] = question.test.course
            context['test'] = question.test
        elif question.quiz:
            context['course'] = question.quiz.lecture.course
            context['lecture'] = question.quiz.lecture
            context['quiz'] = question.quiz
        mcquestion = get_object_or_404(MCQuestion, id=question_id)
        choices = mcquestion.choices.all()
        context['choices'] = collections.OrderedDict()
        context['all_correct_choice'] = []
        i = 0
        for choice in choices:
            context['choices'][chr(65 + i)] = choice
            if choice.correct:
                context['all_correct_choice'].append(str(chr(65 + i)))
            i = i + 1
        if request.method == 'GET':
            context['question_form'] = MCQuestionForm(instance=question)
        if request.method == 'POST':
            question_form = MCQuestionForm(request.POST, request.FILES, instance=mcquestion)
            if question_form.is_valid():
                question_form.save()
                if question.test:
                    return redirect('update_test', test_id=question.test_id)
                elif question.quiz:
                    return redirect('update_quiz', quiz_id=question.quiz_id)
            else:
                context['question_form'] = question_form

    if question.type == 'BF':
        if question.test:
            context['course'] = question.test.course
            context['test'] = question.test
        elif question.quiz:
            context['course'] = question.quiz.lecture.course
            context['lecture'] = question.quiz.lecture
            context['quiz'] = question.quiz
        bfquestion = get_object_or_404(BFQuestion, id=question_id)
        answers = bfquestion.bfquestionanswer_set.all()
        context['answers'] = collections.OrderedDict()
        i = 1
        for answer in answers:
            context['answers'][i] = answer
            i = i + 1
        if request.method == 'GET':
            context['question_form'] = BFQuestionForm(instance=question)
        if request.method == 'POST':
            question_form = BFQuestionForm(request.POST,request.FILES,instance=bfquestion)
            if question_form.is_valid():
                question_form.save()
                if question.test:
                    return redirect('update_test', test_id=question.test_id)
                elif question.quiz:
                    return redirect('update_quiz', quiz_id=question.quiz_id)
            else:
                context['question_form'] = question_form
    return render(request, 'cognita/xinyangg/update_question.html', context)

@login_required
def delete_choice(request):
    context = {}
    choice_id = request.POST.get('choice_id', None)
    choice = get_object_or_404(Choice, id=choice_id)
    mcquestion = choice.mcquestion
    if (mcquestion.choices.count() <= 2):
        context['error_message'] = 'Please leave at least two choices.'
        return JsonResponse(context)
    if (mcquestion.choices.filter(correct__exact=True).count() <=1 and choice.correct == True):
        context['error_message'] = 'Please leave at least one correct choice.'
        return JsonResponse(context)

    if mcquestion.test:
        if request.user == mcquestion.test.course.creator:
            choice.delete()
            context['choice_id'] = choice_id
    elif mcquestion.quiz:
        if request.user == mcquestion.quiz.lecture.course.creator:
            choice.delete()
            context['choice_id'] = choice_id
    return JsonResponse(context)

@login_required
def update_choice(request):
    context = {}
    choice_id = request.POST.get('choice_id', None)
    choice = get_object_or_404(Choice, id=choice_id)
    mcquestion = choice.mcquestion
    correct = request.POST.get('correct', None)
    context['choice_id'] = choice_id
    if (mcquestion.choices.filter(correct__exact=True).count() <= 1 and choice.correct == True and correct == "false"):
        context['error_message'] = 'Please leave at least one correct choice.'
        context['content'] = choice.content
        context['correct'] = choice.correct
        return JsonResponse(context)
    if mcquestion.test:
        if request.user != mcquestion.test.course.creator:
            return JsonResponse(context)
    elif mcquestion.quiz:
        if request.user != mcquestion.quiz.lecture.course.creator:
            return JsonResponse(context)

    if correct == 'true':
        correct = True
    else:
        correct = False
    content = request.POST.get('content', None)
    dict = {'content':content, 'correct':correct}
    choice_form = ChoiceForm(dict,instance=choice)
    if choice_form.is_valid():
        choice_form.save()
    else:
        for error in choice_form.errors:
            context['error_message'] = error
    context['content'] = choice.content
    context['correct'] = choice.correct
    return JsonResponse(context)

@login_required
def add_choice(request):
    context = {}
    question_id = request.POST.get('question_id', None)
    mcquestion = get_object_or_404(MCQuestion, id=question_id)
    correct = request.POST.get('correct', None)

    if mcquestion.test:
        if request.user != mcquestion.test.course.creator:
            return JsonResponse(context)
    elif mcquestion.quiz:
        if request.user != mcquestion.quiz.lecture.course.creator:
            return JsonResponse(context)

    if correct == 'true':
        correct = True
    else:
        correct = False
    content = request.POST.get('content', None)
    dict = {'content': content, 'correct': correct}
    choice_form = ChoiceForm(dict)
    if choice_form.is_valid():
        choice = choice_form.save(commit=False)
        choice.mcquestion = mcquestion
        choice.save()
        context['content'] = choice.content
        context['correct'] = choice.correct
        context['choice_id'] = choice.id
    else:
        for error in choice_form.errors:
            context['error_message'] = error
        context['content'] = content
        context['correct'] = correct
    return JsonResponse(context)

@login_required
def delete_answer(request):
    context = {}
    answer_id = request.POST.get('answer_id', None)
    answer = get_object_or_404(BFQuestionAnswer, id=answer_id)
    bfquestion = answer.bfquestion
    if (bfquestion.bfquestionanswer_set.count() <= 1):
        context['error_message'] = 'Please leave at least one correct answer.'
        return JsonResponse(context)
    if bfquestion.test:
        if request.user == bfquestion.test.course.creator:
            answer.delete()
            context['answer_id'] = answer_id
    elif bfquestion.quiz:
        if request.user == bfquestion.quiz.lecture.course.creator:
            answer.delete()
            context['answer_id'] = answer_id
    return JsonResponse(context)

@login_required
def update_answer(request):
    context = {}
    answer_id = request.POST.get('answer_id', None)
    answer = get_object_or_404(BFQuestionAnswer, id=answer_id)
    bfquestion = answer.bfquestion
    context['answer_id'] = answer_id
    if bfquestion.test:
        if request.user != bfquestion.test.course.creator:
            return JsonResponse(context)
    elif bfquestion.quiz:
        if request.user != bfquestion.quiz.lecture.course.creator:
            return JsonResponse(context)
    answer_content = request.POST.get('answer', None)

    dict = {'answer':answer_content}
    answer_form = BFQuestionAnswerForm(dict, instance=answer)
    if answer_form.is_valid():
        answer_form.save()
    else:
        for error in answer_form.errors:
            context['error_message'] = error
    context['answer'] = answer.answer
    return JsonResponse(context)

@login_required
def add_answer(request):
    context = {}
    question_id = request.POST.get('question_id', None)
    bfquestion = get_object_or_404(BFQuestion, id=question_id)
    if bfquestion.test:
        if request.user != bfquestion.test.course.creator:
            return JsonResponse(context)
    elif bfquestion.quiz:
        if request.user != bfquestion.quiz.lecture.course.creator:
            return JsonResponse(context)
    answer_content = request.POST.get('answer', None)
    dict = {'answer': answer_content}
    answer_form = BFQuestionAnswerForm(dict)
    if answer_form.is_valid():
        answer = answer_form.save(commit=False)
        answer.bfquestion = bfquestion
        answer.save()
        context['answer'] = answer.answer
        context['answer_id'] = answer.id
    else:
        for error in answer_form.errors:
            context['error_message'] = error
        context['answer'] = answer_content
    return JsonResponse(context)

@login_required
def take_test(request, test_id):
    context = {}
    test = get_object_or_404(Test, id=test_id)
    if test.course.published == False:
        return redirect('home')
    if UserAnswerUnsubmit.objects.filter(user=request.user, test=test):
        if UserAnswerUnsubmit.objects.get(user=request.user, test=test).unsubmit == False:
            UserAnswer.objects.filter(user=request.user, question__test=test).delete()
    context['title'] = test.title
    if request.method == 'GET':
        questions = Question.objects.filter(test_id__exact=test_id).order_by('index')
        context = take_quiz_test(context, questions)
        if UserAnswerUnsubmit.objects.filter(user=request.user,test=test):
            if UserAnswerUnsubmit.objects.get(user=request.user,test=test).unsubmit == True:
                for question_dict in context['questions']:
                    try:
                        userAnswer = UserAnswer.objects.get(user=request.user, question_id=question_dict['question'].id)
                        if question_dict['type'] == 'MC':
                            question_dict['saved_answer'] = userAnswer.__str__().split(',')
                        else:
                            question_dict['saved_answer'] = userAnswer
                    except UserAnswer.DoesNotExist:
                        continue
    if request.method == 'POST':
        save_quiz_test_answer(request)
        if request.POST.get('submit', None):
            course_progress = UserProgressCourse.objects.get(user=request.user, course=test.course)
            module = get_object_or_404(Module, id=test_id)
            course_progress.module_completed.add(module)
            course_progress.save()
            if course_progress.module_completed.count() == test.course.module_set.count():
                if course_progress.completed == False:
                    course_progress.completed = True
                    course_progress.save()
            unsubmit, created = UserAnswerUnsubmit.objects.get_or_create(user=request.user, test=test)
            unsubmit.unsubmit = False
            unsubmit.save()
            return redirect('auto_grade_test', test_id=test_id)
    return render(request, 'cognita/xinyangg/take_quiz_test.html', context)

@login_required
def take_quiz(request,quiz_id):
    context = {}
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if quiz.lecture.course.published == False:
        return redirect('home')
    if UserAnswerUnsubmit.objects.filter(user=request.user, quiz=quiz):
        if UserAnswerUnsubmit.objects.get(user=request.user, quiz=quiz).unsubmit == False:
            UserAnswer.objects.filter(user=request.user, question__quiz=quiz).delete()
    context['title'] = quiz.title
    if request.method == 'GET':
        questions = Question.objects.filter(quiz_id__exact=quiz_id).order_by('index')
        context = take_quiz_test(context, questions)
        if UserAnswerUnsubmit.objects.filter(user=request.user,quiz=quiz):
            if UserAnswerUnsubmit.objects.get(user=request.user,quiz=quiz).unsubmit == True:
                for question_dict in context['questions']:
                    try:
                        userAnswer = UserAnswer.objects.get(user=request.user, question_id=question_dict['question'].id)
                        if question_dict['type'] == 'MC':
                            question_dict['saved_answer'] = userAnswer.__str__().split(',')
                        else:
                            question_dict['saved_answer'] = userAnswer
                    except UserAnswer.DoesNotExist:
                        continue
    if request.method == 'POST':
        save_quiz_test_answer(request)
        if request.POST.get('submit', None):
            lecture_progress = get_object_or_404(UserProgressModule,user=request.user, lecture=quiz.lecture)
            course_progress = get_object_or_404(UserProgressCourse, user=request.user, course=quiz.lecture.course)
            part = get_object_or_404(Part, id=quiz_id)
            lecture_progress.part_completed.add(part)
            lecture_progress.save()
            if lecture_progress.part_completed.count() == quiz.lecture.part_set.count():
                if lecture_progress.completed == False:
                    lecture_progress.completed = True
                    lecture_progress.save()
                    module = get_object_or_404(Module, id=quiz.lecture.id)
                    course_progress.module_completed.add(module)
                    course_progress.save()
                    if course_progress.module_completed.count() == quiz.lecture.course.module_set.count():
                        course_progress.completed = True
                        course_progress.save()
            unsubmit, created = UserAnswerUnsubmit.objects.get_or_create(user=request.user, quiz=quiz)
            unsubmit.unsubmit = False
            unsubmit.save()
            return redirect('auto_grade_quiz', quiz_id=quiz_id)
    return render(request, 'cognita/xinyangg/take_quiz_test.html', context)

def take_quiz_test(context, questions):
    context['questions'] = []
    for question in questions:
        if question.type == 'MC':
            mcquestion = MCQuestion.objects.get(id=question.id)
            correct = 0
            count = 0
            choices_dict = collections.OrderedDict()
            for choice in mcquestion.choices.all():
                choices_dict[chr(count + 65)] = choice
                count = count + 1
                if choice.correct:
                    correct = correct + 1
            if correct > 1:
                input_type = 'checkbox'
            else:
                input_type = 'radio'
            context['questions'].append(
                {'type': 'MC', 'question': mcquestion, 'input_type': input_type, 'choices': choices_dict})
        else:
            bfquestion = BFQuestion.objects.get(id=question.id)
            context['questions'].append({'type': 'BF', 'question': bfquestion})
    context['question_list'] = range(1, questions.count() + 1, 1)
    return context

@login_required
def save_quiz_test_answer(request):
    for key in request.POST.iterkeys():
        find_mc = re.match(r'^question_(?P<question_id>[0-9]+)_choice$', key)
        if find_mc:
            choices = request.POST.getlist(key)
            question = get_object_or_404(Question, id=find_mc.group('question_id'))
            mcquestion = get_object_or_404(MCQuestion, id=find_mc.group('question_id'))
            choice_list = []
            for choice in mcquestion.choices.all():
                choice_list.append(str(choice.id))
            for user_choice in choices:
                if user_choice not in choice_list:
                    choices.remove(user_choice)

            user_choices, created = UserAnswer.objects.get_or_create(user=request.user, question=question)
            user_choices.type = 'MC'
            user_choices.answer = ",".join(choices)
            user_choices.save()

        find_bf = re.match(r'^question_(?P<question_id>[0-9]+)_blank$', key)
        if find_bf:
            answer = request.POST.get(key, None)
            if answer and answer != '':
                question = get_object_or_404(Question, id=find_bf.group('question_id'))
                user_bf_answer_form = UserBFAnswerForm({'answer': answer})
                if user_bf_answer_form.is_valid():
                    user_bf_answer, created = UserAnswer.objects.get_or_create(user=request.user, question=question, type='BF')
                    user_bf_answer.answer = user_bf_answer_form.cleaned_data['answer']
                    user_bf_answer.save()
    if request.POST.get('submit', None) is None:
        if request.POST.get('quiz_or_test') == 'take_test':
            unsubmit, created = UserAnswerUnsubmit.objects.get_or_create(user=request.user, test_id=int(request.POST.get('quiz_or_test_id')))
            if unsubmit.unsubmit == False:
                unsubmit.unsubmit = True
                unsubmit.save()
        if request.POST.get('quiz_or_test') == 'take_quiz':
            unsubmit, created = UserAnswerUnsubmit.objects.get_or_create(user=request.user, quiz_id=int(request.POST.get('quiz_or_test_id')))
            if unsubmit.unsubmit == False:
                unsubmit.unsubmit = True
                unsubmit.save()
        return JsonResponse({})

@login_required
def auto_grade_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if test.course.published == False:
        return redirect('home')
    umsub = UserAnswerUnsubmit.objects.filter(user=request.user, test=test)
    if (not umsub) or UserAnswerUnsubmit.objects.get(user=request.user, test=test).unsubmit == True:
        return redirect('take_test', test_id=test_id)
    context = {}
    context['title'] = test.title
    context['course'] = test.course
    context['full_score'] = test.full_score
    context = auto_grade_test_quiz(request, context, test.questions.all().order_by('index'))
    user_grade, created = Grade.objects.get_or_create(user=request.user, test=test)
    user_grade.grade = context['user_grade']
    user_grade.save()
    return render(request, 'cognita/xinyangg/auto_grade.html', context)

@login_required
def auto_grade_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if quiz.lecture.course.published == False:
        return redirect('home')
    umsub = UserAnswerUnsubmit.objects.filter(user=request.user, quiz=quiz)
    if (not umsub) or UserAnswerUnsubmit.objects.get(user=request.user, quiz=quiz).unsubmit == True:
        return redirect('take_quiz', quiz_id=quiz_id)
    context = {}
    context['title'] = quiz.title
    context['course'] = quiz.lecture.course
    context['full_score'] = quiz.full_score
    context = auto_grade_test_quiz(request, context, quiz.questions.all().order_by('index'))
    user_grade, created = Grade.objects.get_or_create(user=request.user, quiz=quiz)
    user_grade.grade = context['user_grade']
    user_grade.save()
    return render(request, 'cognita/xinyangg/auto_grade.html', context)

@login_required
def auto_grade_test_quiz(request,context, questions):
    user_weight = 0
    total_weight = 0
    i = 0
    context['questions'] = []
    for question in questions:
        total_weight = total_weight + question.weight
        question_dict = {}
        question_dict['question'] = question
        i = i + 1
        if question.type == 'MC':
            question_dict['type'] = 'MC'
            mcquestion = get_object_or_404(MCQuestion, id=question.id)
            try:
                user_choice_ids = UserAnswer.objects.get(question__exact=question,
                                                         user__exact=request.user).__str__().split(',')
            except UserAnswer.DoesNotExist:
                user_choice_ids = [-1]
            try:
                user_choice_ids = [int(i) for i in user_choice_ids]
            except:
                user_choice_ids = [-1]
            user_choice_list = Choice.objects.filter(id__in=user_choice_ids)
            question_dict['user_choices'] = user_choice_list
            correct_choice_list = mcquestion.choices.filter(correct=True).values()
            question_dict['correct_choices'] = correct_choice_list
            correct_choice_id_list = mcquestion.choices.filter(correct=True).values_list('id', flat=True)[::1]
            correct_choice_id_list = [str(x) for x in correct_choice_id_list]
            if user_choice_ids == correct_choice_id_list:
                user_weight = user_weight + question.weight
                question_dict['correct'] = True
            else:
                question_dict['correct'] = False
            context['questions'].append(question_dict)

        else:
            question_dict['type'] = 'BF'
            bfquestion = get_object_or_404(BFQuestion, id=question.id)
            try:
                user_answer = UserAnswer.objects.get(question__exact=question, user__exact=request.user)
            except UserAnswer.DoesNotExist:
                user_answer = []
            question_dict['user_answers'] = user_answer
            question_dict['correct_answers'] = bfquestion.bfquestionanswer_set.all()
            if user_answer.__str__() in bfquestion.bfquestionanswer_set.all().values_list('answer', flat=True):
                user_weight = user_weight + question.weight
                question_dict['correct'] = True
            else:
                question_dict['correct'] = False
            context['questions'].append(question_dict)
    context['user_grade'] = round(context['full_score'] * user_weight / total_weight, 1)
    return context

@login_required
def reorder_questions(request):
    question_dict ={}
    for key in request.POST.iterkeys():
        find = re.match(r'^question_ids\[(?P<question_id>[0-9]+)\]$', key)
        if find:
            question = get_object_or_404(Question, id=request.POST.get(key, None))
            question_dict[find.group('question_id')] = question
    if request.POST.get('type') == 'test':
        test = get_object_or_404(Test, id=request.POST.get('id'))
        if test.course.creator != request.user:
            return redirect('home')
        if question_dict.values().sort() != test.questions.all()[::1].sort():
            return redirect('update_test', test_id=test.id)
    elif request.POST.get('type') == 'quiz':
        quiz = get_object_or_404(Quiz, id=request.POST.get('id'))
        if quiz.lecture.course.creator != request.user:
            return redirect('home')
        if question_dict.values().sort() != quiz.questions.all()[::1].sort():
            return redirect('update_quiz', quiz_id=quiz.id)
    else:
        return redirect('home')
    for index, question in question_dict.items():
        question.index = int(index) + 1
        question.save()
    return JsonResponse({})

@login_required
def get_question_image(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if not question.image:
        raise Http404
    content_type = guess_type(question.image.name)
    return HttpResponse(question.image, content_type=content_type)
