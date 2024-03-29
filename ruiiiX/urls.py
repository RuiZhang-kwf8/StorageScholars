"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),
    path('userdashboard/', TemplateView.as_view(template_name="userdashboard.html")),
    path("chat/<str:chat_box1>/", views.chat_box, name="chat"),
    path('findhousing/', views.housing, name = "housing"),
    path('listing/', views.report, name="listing"),
    path('save_marker/', views.modelmarker, name="save_marker"),
    path('get_markers/', views.get_markers, name="get_markers"),
    path('logout', LogoutView.as_view()),
]