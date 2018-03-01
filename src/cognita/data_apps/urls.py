from django.conf.urls import url
from django.contrib import admin
from data_apps import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^get_try$', views.get_try),
]