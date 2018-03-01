from django.conf.urls import url
from cognita import views_shiqiw
from cognita.views_shiqiw import LoginView, RegisterView, self_profle,\
    logout_view, course_page, course_content, view_course_reading, \
    toggle_register, registerButton, toggle_progress, get_course_img,\
    get_instructor_page, cognita_home, get_note, save_note

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^profile/$',self_profle, name='self_profile'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^course/(?P<course_id>\d+)/$',course_page, name='course_page'),
    url(r'^coursecontent/(?P<course_id>\d+)/$',course_content, name='course_content'),
    url(r'^viewcoursereading/(?P<reading_id>\d+)$', view_course_reading, name='view_course_reading'),
    url(r'^registerbutton/(?P<course_id>\d+)$', registerButton, name='registerButton'),
    url(r'^toggleregister/$',toggle_register,name='toggle_register'),
    url(r'^toggleprogress/$', toggle_progress, name ='toggle_progress'),
    url(r'^getcourseimg/(?P<course_id>\d+)$', get_course_img,name='course_img' ),
    url(r'^instructor/(?P<user_id>\d+)$',get_instructor_page, name='instructor'),
    url(r'^$', cognita_home, name='home'),
    url(r'^getnote/(?P<lecture_id>\d+)$', get_note, name='getnote'),
    url(r'^savenote/$', save_note, name='savenote')
]