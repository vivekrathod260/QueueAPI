from django.contrib import admin
from django.urls import path, include
from LineApp import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('protected/', views.protected, name="protected"),
    path('joinqueue', views.joinqueue, name="joinqueue"),
    path('exitqueue', views.exitqueue, name="exitqueue"),
    path('myjoinedqueue', views.myjoinedqueue, name="myjoinedqueue"),
    path('createqueue', views.createqueue, name="createqueue"),
    path('myqueue', views.myqueue, name="myqueue"),
    path('deletequeue', views.deletequeue, name="deletequeue"),
    path('customerpanel', views.customerpanel, name="customerpanel"),
    path('adminpanel', views.adminpanel, name="adminpanel"),
    path('pop', views.pop, name="pop"),
    path('deletepersonfromqueue', views.deletepersonfromqueue, name="deletepersonfromqueue"),
]