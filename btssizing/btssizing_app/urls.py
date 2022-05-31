from django.urls import path, include

from . import views

app_name = 'btssizing_app'

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('', views.dashboard, name='index'),
    path('home/', views.dashboard, name='home'),
    path('users/', views.users, name='users'),
]