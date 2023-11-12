from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('schedule_keeper.urls')),
    path('admin/', admin.site.urls),
]
