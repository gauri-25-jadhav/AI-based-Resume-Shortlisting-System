from django.urls import path
from .views import candidate_register, login_view

urlpatterns = [
    path('register/', candidate_register, name='register'),
    path('login/', login_view, name='login'),
]
