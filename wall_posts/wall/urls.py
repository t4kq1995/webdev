"""
wall URL Configuration
"""
from django.conf.urls import url, include
from wall import views

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', views.MessageView.as_view(), name='index'),
]
