from mimetypes import guess_type

from django.db.models import Count
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from cognita.forms_shiqiw import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cognita.models import *

class LoginView(View):
    template_name = 'cognita/users/login.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('home')
        else:
            login_form = LoginForm()
            return render(request, self.template_name, {'form': login_form})


    def post(self,request):
        if request.user.is_authenticated():
            return redirect('home')
        else:
            context = {}
            form = LoginForm(request.POST)
            if form.is_valid():
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                user = authenticate(username=username, password=password)
                # if user is authenticated
                if user:
                    login(request, user)
                    return redirect('home')
                else:
                    context['login_failure'] = 'Login failed, please check username and password'
                    context['form'] = LoginForm()
                    return render(request, self.template_name, context)
            else:
                context['form'] = form
                return render(request, self.template_name, context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


class RegisterView(View):
    register_form = RegisterForm()
    template_name = 'cognita/users/register.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('home')
        else:
            return render(request, self.template_name, {'form': self.register_form})

    def post(self, request):
        if request.user.is_authenticated():
            return redirect('home')
        else:
            register_form = RegisterForm(request.POST)
            # validate the form data
            if register_form.is_valid():
                form = RegisterForm(request.POST)
                new_user = form.save(commit=False)
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                new_user.set_password(password)
                new_user.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('home')

            else:
                return render(request, self.template_name, {'form': register_form})


@login_required
def self_profle(request):
    if request.method == "GET":
        context = {}
        username = request.user.username
        user = get_object_or_404(User, username=username)
        context['courses_taking'] = user.course_taking.all().order_by('category').order_by('created_at')
        context['courses_created'] = user.course_created.all().order_by('category').order_by('created_at')

        courses = user.course_taking.all().order_by('category').order_by('created_at')
        # get grade for each course
        grade_list = []
        for course in courses:
            grades_quiz = user.grade_set.filter(quiz__lecture__course=course)
            grades_test = user.grade_set.filter(test__course=course)
            ave_grade = 0
            for grade in grades_quiz:
                ave_grade = ave_grade + (grade.grade/float(grade.quiz.full_score))*100
            for grade in grades_test:
                ave_grade = ave_grade + (grade.grade/float(grade.test.full_score))*100
            total_count = grades_test.count()+grades_quiz.count()
            if total_count > 0:
                ave_grade = ave_grade / total_count

            # completed_mod_num = user.userprogressmodule_set.filter(lecture__course=course, completed=True).count()
            course_completion = False
            if user.userprogresscourse_set.filter(course=course).count() == 1:
                course_completion = user.userprogresscourse_set.filter(course=course)[0].completed
            course_info = (int(ave_grade), course_completion)
            grade_list.append([course, course_info])
            #print course_info
        context['courses_taking_grade'] = grade_list
        return render(request, 'cognita/users/self_profile.html', context)

@login_required
def course_page(request, course_id):
    if request.method == "GET":
        context = {}
        course = get_object_or_404(Course, id = course_id)
        user = get_object_or_404(User, username=request.user.username)
        if not course.published:
            raise Http404
        context['course'] = course
        return render(request, 'cognita/student/course_base.html', context)

@login_required
def registerButton(request, course_id):
    if request.method == "GET":
        context = {}
        course = get_object_or_404(Course, id=course_id)
        user = get_object_or_404(User, username=request.user.username)
        if user.course_taking.filter(id=course_id).count() == 1:
            context['form_action'] = 'Drop'
        else:
            context['form_action'] = 'Register'
        context['register_form'] = RegisterCourseForm(initial={'course': course_id})
        return render(request, 'cognita/student/register_form.html',context)


@login_required
def course_content(request, course_id):
    if not course_id.isdigit():
        return Http404
    if request.method == "GET":
        course = get_object_or_404(Course, id=course_id)
        user = get_object_or_404(User, username=request.user.username)
        modules = course.module_set.all().order_by('index')
        context = {}
        context['modules'] = modules
        if user.course_taking.filter(id=course_id).count() == 1:
            context['taking'] = True
            ##TODO
            progressmodules = user.userprogressmodule_set.filter(lecture__course=course)
            #print('****************')
            #print(progressmodules.count())
            progress_list = []
            for progressmodule in progressmodules:
                lecture = get_object_or_404(Lecture, id=progressmodule.lecture.id)
                #print(lecture.title)
                part_progress = progressmodule.part_completed.all()
                for part in lecture.part_set.all():
                    if part in part_progress:
                        #print('part in '+part.title)
                        progress_list.append([part.id, 1])
                    else:
                        #print('part out '+part.title)
                        progress_list.append([part.id, 0])
            context['progress_list'] = progress_list
        else:
            context['taking'] = False
        html = render_to_string('cognita/student/course_content.html', context)
        return HttpResponse(html)

@login_required
def view_course_reading(request, reading_id):
    reading = get_object_or_404(Reading, id=reading_id)
    if reading.lecture.course.students.filter(id=request.user.id).count() == 0:
        raise Http404
    if not reading.file:
        raise Http404

    content_type = 'application/pdf'
    response = HttpResponse(reading.file, content_type=content_type)
    response['Content-Disposition'] = 'inline'
    return response

@login_required
def toggle_register(request):
    if request.method == "POST":
        course_id = request.POST.get('course', '0')
        course = get_object_or_404(Course, id=course_id)

        register_form = RegisterCourseForm(request.POST)
        if register_form.is_valid():
            if course.students.filter(id=request.user.id).count() == 0:
                course.students.add(request.user)
                # create UserProgressCourse object
                UserProgressCourse.objects.get_or_create(user=request.user,course=course)
                # create UserProgressModule object
                for module in course.module_set.all().order_by('index'):
                    if module.module_type == 'L':
                        UserProgressModule.objects.get_or_create(user=request.user,lecture=module.lecture)

            elif course.students.filter(id=request.user.id).count() == 1:
                course.students.remove(request.user)

    return HttpResponse(status=200)

@login_required
def toggle_progress(request):
    if request.method == 'POST':
        part_id = request.POST.get('part', '0')
        #print(part_id)
        part = get_object_or_404(Part, id=part_id)
        result = ''
        progress_form = ProgressForm(request.POST)
        if progress_form.is_valid():
            #print('valid')
            # we have the part id, and the user, now we need to see if this part is completed
            lecture = part.lecture
            myProgressModule = get_object_or_404(UserProgressModule, user=request.user, lecture=lecture)
            myProgressCourse = get_object_or_404(UserProgressCourse, user=request.user, course=lecture.course)
            if part.completed_part.filter(user=request.user).count() == 0:
                #print('add to completed part')
                myProgressModule.part_completed.add(part)
                myProgressModule.save()
                result = 'Completed'
            else:
                #print('remove from completed part')
                myProgressModule.part_completed.remove(part)
                myProgressModule.save()
                result = 'Mark as Complete'
                myProgressCourse.module_completed.remove(lecture)
            # check if all parts in the module has been completed
            if myProgressModule.part_completed.count() == lecture.part_set.count():
                # print('completed part number: ')
                # print(myProgressModule.part_completed.count())
                # print('total part number: ')
                # print(lecture.part_set.count())
                # print('set to true')
                myProgressModule.completed = True
                myProgressModule.save()
                myProgressCourse.module_completed.add(lecture)
                myProgressCourse.save()
                # print("*****")
                # print(myProgressCourse.module_completed.count())
                # print("^^^^^")
                # print(lecture.course.module_set.count())
                if myProgressCourse.module_completed.count() == lecture.course.module_set.count():
                    myProgressCourse.completed = True
                    myProgressCourse.save()

            else:
                # print('completed part number: ')
                # print(myProgressModule.part_completed.count())
                # print('total part number: ')
                # print(lecture.part_set.count())
                myProgressModule.completed = False
                myProgressModule.save()
                # print("*****")
                # print(myProgressCourse.module_completed.count())
                # print("^^^^^")
                # print(lecture.course.module_set.count())
                myProgressCourse.completed = False
                myProgressCourse.save()

        else:
            pass
            # print('invalid')
    return HttpResponse(result)

@login_required
def get_course_img(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not course.course_image:
        raise Http404

    content_type = guess_type(course.course_image.name)
    return HttpResponse(course.course_image, content_type=content_type)

@login_required
def get_instructor_page(request, user_id):
    user= get_object_or_404(User, id=user_id)
    courses = user.course_created.filter(published=True)
    context = {}
    context['instructor'] = user
    context['courses'] = courses
    return render(request, 'cognita/users/instructor_profile.html', context)

@login_required
def cognita_home(request):
    course_list = []
    # order by category, only published, then by number of students, choose top 3
    # for each category, has a detailed page
    # category list:
    Category_CHOICES = ['CS', 'MATH','ART', 'BUS', 'SCI', 'SSCI', 'LIT', 'UCL']
    for cat in Category_CHOICES:
        top_3_courses = Course.objects.filter(category__exact=cat, published=True).annotate(count=Count('students')).order_by('-count')[:3]
        course_list.append([cat, top_3_courses])
    #print course_list
    context = {}
    context['course_list'] = course_list
    return render(request, 'cognita/users/homepage.html', context)

@login_required
def get_note(request, lecture_id):
    # get or create note model for this lecture
    # create a form to show is content
    # return the form
    if not lecture_id.isdigit():
        return Http404
    lecture = get_object_or_404(Lecture, id=lecture_id)
    (note,created) = StudentNote.objects.get_or_create(user=request.user, lecture=lecture)
    context = {}
    context['note'] = note
    return render(request, 'cognita/student/note_form.html', context)

@login_required
def save_note(request):
    if request.method == "POST":
        lecture_id = request.POST.get('lecture_id', '0')
        if not lecture_id.isdigit() or (Lecture.objects.filter(id=lecture_id).count() != 1):
            return HttpResponse("save error")
        lecture = get_object_or_404(Lecture, id=lecture_id)
        if StudentNote.objects.filter(user=request.user,lecture=lecture).count() != 1:
            return HttpResponse("save error")
        instance = get_object_or_404(StudentNote, user=request.user, lecture=lecture)
        note_form = NoteForm(request.POST, instance=instance)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.lecture = lecture
            note.user = request.user
            note.save()
            return HttpResponse("saved")
        else:
            #print("form invalid")
            #print(note_form.errors)
            return HttpResponse("save error")
    return HttpResponse("save error")