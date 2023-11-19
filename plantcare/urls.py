from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import profile

urlpatterns = [
    path('', include('schedule_keeper.urls')),
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='accounts')),
    path('accounts/profile/', profile, name='profile'),
    path('admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
