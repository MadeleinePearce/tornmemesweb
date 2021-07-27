from django.urls import path

from webportal.views import *

urlpatterns = [
    path("", homepage),
    path("sponsors", sponsorspage),
    path("api/v1/login", loginapi),
    path("api/v1/reactions", memereactions),
]
