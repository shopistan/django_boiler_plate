"""
User app urls
"""
from django.conf.urls import include, url
from django.urls import re_path
from rest_auth.registration.views import VerifyEmailView
from rest_framework import routers

from . import views
from .views import (UserViewSet,
                    GroupViewSet)

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, 'user')
router.register(r'group', GroupViewSet, 'group')
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
    re_path(r'^permissions/$', views.getPermissions, name='permissions'),
    re_path(r'^userpermissions/$', views.getUserPermissions, name='userpermissions'),
    re_path(r'^rolespermissions/', views.getallRolesPermissions, name='rolepermissions'),
    
]
