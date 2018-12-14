from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^register$', views.register),
    url(r'^logout$', views.log_out),
    url(r'^log_in$', views.login),
    url(r'^wall$', views.wall),
    url(r'^login_wall$', views.login_wall),
    url(r'^leave$', views.leave),
    url(r'^post$', views.post),
    url(r'^post_comment/(?P<id>\d+)$', views.post_comment),
    url(r'^delete/(?P<id>\d+)$',views.delete),
]