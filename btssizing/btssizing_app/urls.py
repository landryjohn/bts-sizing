from django.urls import path, include

from . import views

app_name = 'btssizing_app'

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('', views.dashboard, name='index'),
    path('home/', views.dashboard, name='home'),
    path('users/', views.users, name='users'),
    path('projects/', views.projects, name='projects'),
    path('projects/add/', views.add_project, name='add_project'),
    path('plan_couverture/', views.plan_couverture, name='plan_couverture'),
    path('add_plan_couverture/', views.add_plan_couverture, name='add_plan_couverture')
]