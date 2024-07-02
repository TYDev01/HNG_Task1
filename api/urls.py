from .views import hello
from django.urls import path

urlpatterns = [
    path('api/hello/', hello)
]