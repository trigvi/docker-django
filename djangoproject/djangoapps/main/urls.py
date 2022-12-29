from django.contrib import admin
from django.urls import include, path
from . import views

admin.site.site_header  = "Django Project"
admin.site.site_title   = "Django Project"
admin.site.index_title  = "Welcome to Django Project"

urlpatterns = [
    path("admin/", admin.site.urls),
]
