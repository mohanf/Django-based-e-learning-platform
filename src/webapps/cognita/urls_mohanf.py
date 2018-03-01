from django.conf.urls import url
import cognita.views_mohanf


urlpatterns = [
    url(r'^add_course$', cognita.views_mohanf.add_course, name='add_course'),
    url(r'^creating_course/(?P<course_id>\d+)$', cognita.views_mohanf.creating_course, name='creating_course'),
    url(r'^add_lecture/(?P<course_id>\d+)$', cognita.views_mohanf.add_lecture, name='add_lecture'),
    url(r'^add_reading/(?P<lecture_id>\d+)$', cognita.views_mohanf.add_reading, name='add_reading'),
    url(r'^add_video/(?P<lecture_id>\d+)$', cognita.views_mohanf.add_video, name='add_video'),
    url(r'^modify_course/(?P<course_id>\d+)$', cognita.views_mohanf.modify_course, name='modify_course'),
    url(r'^view_part/(?P<part_id>\d+)$', cognita.views_mohanf.view_part, name='view_part'),
    url(r'^get_reading/(?P<reading_id>\d+)$', cognita.views_mohanf.get_reading, name='get_reading'),
    url(r'^modify_lecture/(?P<lecture_id>\d+)$', cognita.views_mohanf.modify_lecture, name='modify_lecture'),
    url(r'^modify_reading/(?P<reading_id>\d+)$', cognita.views_mohanf.modify_reading, name='modify_reading'),
    url(r'^modify_video/(?P<video_id>\d+)$', cognita.views_mohanf.modify_video, name='modify_video'),
    url(r'^delete_part$', cognita.views_mohanf.delete_part, name='delete_part'),
    url(r'^delete_module$', cognita.views_mohanf.delete_module, name='delete_module'),
    url(r'^publish/(?P<course_id>\d+)$', cognita.views_mohanf.publish, name='publish'),
    url(r'^reorder_part/(?P<lecture_id>\d+)$', cognita.views_mohanf.reorder_part, name='reorder_part'),
    url(r'^reorder_module/(?P<course_id>\d+)$', cognita.views_mohanf.reorder_module, name='reorder_module'),
    url(r'^search$', cognita.views_mohanf.search, name='search'),
    url(r'^search_with_option$', cognita.views_mohanf.search_with_option, name='search_with_option'),
    url(r'^add_material/(?P<lecture_id>\d+)$', cognita.views_mohanf.add_material, name='add_material'),
    url(r'^start_material/(?P<reading_id>\d+)$', cognita.views_mohanf.start_material, name='start_material'),
    url(r'^modify_material/(?P<reading_id>\d+)$', cognita.views_mohanf.modify_material, name='modify_material'),
    url(r'^save_material/(?P<reading_id>\d+)$', cognita.views_mohanf.save_material, name='save_material'),
    url(r'^add_tag/(?P<course_id>\d+)$', cognita.views_mohanf.add_tag, name='add_tag'),
    url(r'^complete$', cognita.views_mohanf.complete, name="complete"),
    url(r'^delete_tag/(?P<course_id>\d+)$', cognita.views_mohanf.delete_tag, name='delete_tag'),
]