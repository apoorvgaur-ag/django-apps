from django.urls import path

from .views import (
		LoginView,
)


APP_NAME = 'user'
urlpatterns = [
	path('login/',LoginView.as_view() , name='login'),
]
