from django.urls import path

from webportal.views import *

urlpatterns = [
    path("", homepage),
]
