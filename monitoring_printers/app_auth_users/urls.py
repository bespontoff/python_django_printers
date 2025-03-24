from django.urls import path
from .views import *


urlpatterns = [
    path('another_login/', login_view, name='another_login'),
    path('login/', AnotherLoginView.as_view(), name='login'),
]

