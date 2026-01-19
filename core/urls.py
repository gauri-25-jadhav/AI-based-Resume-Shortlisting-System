from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    #path('select-role/', views.login_selection, name='login_selection'),
    path('login/', views.login_selection, name='login_selection'),
    path('login/candidate/', views.candidate_login, name='candidate_login'),
    path('login/hr/', views.hr_login, name='hr_login'),
    path('dashboard/candidate/', views.candidate_dashboard, name='candidate_dashboard'),
    path('dashboard/hr/', views.hr_dashboard, name='hr_dashboard'),

]
