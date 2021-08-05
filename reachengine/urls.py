# reachengine/urls.py
from django.conf.urls import url
from reachengine import views
from django.urls import path

urlpatterns = [
	url('^$', views.HomePageView.as_view()),
	path('index/', views.get_hashtags, name="fetchHashTag")
]