''' This file is used to define the URL patterns for the wiki app. '''
from django.urls import path
from . import views

# Define the URL patterns for the wiki app
urlpatterns = [
    path('', views.index, name='index'),
    path('wiki/<str:title>/', views.view_entry, name='view_entry'),
    path('create/', views.create, name='create'),
    path('edit/<str:title>/', views.edit_entry, name='edit_entry'),
    path('random/', views.random_entry, name='random_entry'),
    path('search/', views.search, name='search')
]
