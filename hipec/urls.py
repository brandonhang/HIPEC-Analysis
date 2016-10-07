from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^hipec-app/$', views.hipec_app, name='hipec_app'),
]