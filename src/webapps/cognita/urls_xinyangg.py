from django.conf.urls import url
from cognita import views_xinyangg

urlpatterns = [
    url(r'^(?P<course_id>[0-9]+)/create_test/$', views_xinyangg.create_test, name='create_test'),
    url(r'^(?P<lecture_id>[0-9]+)/create_quiz/$', views_xinyangg.create_quiz, name='create_quiz'),
    url(r'^update_test/(?P<test_id>[0-9]+)/$', views_xinyangg.update_test, name='update_test'),
    url(r'^update_test_info/(?P<test_id>[0-9]+)/$', views_xinyangg.update_test_info, name='update_test_info'),
    url(r'^update_quiz/(?P<quiz_id>[0-9]+)/$', views_xinyangg.update_quiz, name='update_quiz'),
    url(r'^update_quiz_info/(?P<quiz_id>[0-9]+)/$', views_xinyangg.update_quiz_info, name='update_quiz_info'),
    url(r'^create_question_test/(?P<test_id>[0-9]+)/$', views_xinyangg.create_question_test, name='create_question_test'),
    url(r'^create_question_quiz/(?P<quiz_id>[0-9]+)/$', views_xinyangg.create_question_quiz, name='create_question_quiz'),
    url(r'^update_question/(?P<question_id>[0-9]+)/$', views_xinyangg.update_question, name='update_question'),
    url(r'^delete_question/$', views_xinyangg.delete_question, name='delete_question'),
    url(r'^reorder_questions/$', views_xinyangg.reorder_questions, name='reorder_questions'),
    url(r'^delete_choice/$', views_xinyangg.delete_choice, name='delete_choice'),
    url(r'^update_choice/$', views_xinyangg.update_choice, name='update_choice'),
    url(r'^add_choice/$', views_xinyangg.add_choice, name='add_choice'),
    url(r'^delete_answer/$', views_xinyangg.delete_answer, name='delete_answer'),
    url(r'^update_answer/$', views_xinyangg.update_answer, name='update_answer'),
    url(r'^add_answer/$', views_xinyangg.add_answer, name='add_answer'),
    url(r'^take_test/(?P<test_id>[0-9]+)/$', views_xinyangg.take_test, name='take_test'),
    url(r'^take_quiz/(?P<quiz_id>[0-9]+)/$', views_xinyangg.take_quiz, name='take_quiz'),
    url(r'^save_quiz_test_answer/$', views_xinyangg.save_quiz_test_answer, name='save_test_user_answer'),
    url(r'^auto_grade_test/(?P<test_id>[0-9]+)/$', views_xinyangg.auto_grade_test, name='auto_grade_test'),
    url(r'^auto_grade_quiz/(?P<quiz_id>[0-9]+)/$', views_xinyangg.auto_grade_quiz, name='auto_grade_quiz'),
    url(r'^get_question_image/(?P<question_id>[0-9]+)/$', views_xinyangg.get_question_image, name='get_question_image')
]