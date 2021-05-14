from django.conf.urls import url
from .views import *


urlpatterns = [

    url(r'^advisor/', CreateAdvisor.as_view()),
    url(r'^register/', CreateUser.as_view()),
    url(r'^login/', Login.as_view()),
    url(r'^(?P<user_id>\d+)/advisor$', Advisorlist.as_view()),
    url(r'^(?P<user_id>\d+)/advisor/(?P<advisor_id>\d+)/$', BookCall.as_view()),
    url(r'^(?P<user_id>\d+)/advisor/booking/$', BookingDetails.as_view()),

]