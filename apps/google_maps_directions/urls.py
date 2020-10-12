from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^enter$', views.enter, name="enter"),
    url(r'^enter_trip$', views.enter_trip, name="enter_trip"),
]