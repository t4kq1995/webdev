"""
wall URL Configuration
"""
from django.conf.urls import url, include
from wall import views

urlpatterns = [
    url(r'^$', views.login_page, name='check'),
]
