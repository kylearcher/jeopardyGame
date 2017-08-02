from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^double', views.double, name='double'),
    url(r'^final', views.final, name='final'),
    ]
