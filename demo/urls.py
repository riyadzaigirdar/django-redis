from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [ 
    path('', views.manage_keys),
    path('<slug:key>', views.manage_key)
]
