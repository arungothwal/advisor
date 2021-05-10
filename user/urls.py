from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^advisor/', CreateAdvisor.as_view()),
]