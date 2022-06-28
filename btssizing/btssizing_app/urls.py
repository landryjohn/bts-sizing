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
    path('add_plan_couverture/', views.add_plan_couverture, name='add_plan_couverture'),
    path('show_plan_couverture/<int:id>', views.show_plan_couverture, name='show_plan_couverture'),
    path('edit_plan_couverture/<int:id>', views.edit_plan_couverture, name='edit_plan_couverture'),
    path('plan_capacite/', views.plan_capacite, name='plan_capacite'),
    path('add_plan_capacite/', views.add_plan_capacite, name='add_plan_capacite'),
    path('show_plan_capacite/<int:id>', views.show_plan_capacite, name='show_plan_capacite'),
    path('edit_plan_capacite/<int:id>', views.edit_plan_capacite, name='edit_plan_capacite'),
]