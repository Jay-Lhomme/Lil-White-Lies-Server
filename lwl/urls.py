"""lwl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from rest_framework import routers
from django.conf.urls import include
from lwlapi.views import check_user, register_user, StoryView, GroupView, IndividualView, UserView, GroupStoryView, IndividualStoryView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'storys', StoryView, 'story')
router.register(r'groups', GroupView, 'group')
router.register(r'individuals', IndividualView, 'individual')
router.register(r'users', UserView, 'user')
router.register(r'individualstorys', IndividualStoryView, 'individualstory')
router.register(r'groupstorys', GroupStoryView, 'groupstory')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('checkuser', check_user, name='check_user'),
    path('registeruser', register_user),
]
