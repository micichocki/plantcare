from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='main-view'),
    path('plants/', views.plants, name='plants'),
    path('plants/<int:pk>/', views.plant_detail, name='plant-detail'),
    path('plants/<int:plant_pk>/posts/new/', views.post_edit, name='post-create'),
    path('plants/<int:plant_pk>/posts/<int:post_pk>/', views.post_edit, name='post-edit'),
]
