from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main-view'),
    path('plants/', views.plants, name='plants'),
    path('plants/new/', views.PlantView.as_view(), name='plant-create'),
    path('plants/<int:pk>/', views.plant_detail, name='plant-detail'),
    path('plants/<int:pk>/edit/', views.PlantEditView.as_view(), name='plant-edit'),
    path('follow-plant/<int:plant_id>/', views.follow_plant, name='follow-plant'),
    path('plants/<int:plant_pk>/posts/new/', views.PostView.as_view(), name='post-create'),
    path('plants/<int:plant_pk>/posts/<int:post_pk>/', views.PostView.as_view(), name='post-edit'),
]
