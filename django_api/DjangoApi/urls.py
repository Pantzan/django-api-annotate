from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', include('api_annotate.urls')),
    path('admin/', admin.site.urls),
]
