"""
flashcards URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from rest_framework import routers
from flashcardsapi.views import register, login, CategoryQuestions, Categories, UserViewSet, Questions


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', UserViewSet, 'user')
router.register(r'categoryquestions', CategoryQuestions, 'categoryquestion')
router.register(r'categories', Categories, 'category')
router.register(r'questions', Questions, 'question')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register),
    path('login', login),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework'))

]
