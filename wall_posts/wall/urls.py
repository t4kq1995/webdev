"""
wall URL Configuration
"""
from django.conf.urls import url, include
from wall import views

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='check'),
    url(r'^accounts/', include('allauth.urls')),
]
