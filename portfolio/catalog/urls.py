from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectsListView.as_view(), name='index'),
    path('category/<str:category_name>', 
        views.CategoryListView.as_view(), 
        name='category_view'),
    path('technology/<str:technology_name>', 
        views.TechnologyListView.as_view(), 
        name='technology_view'),
    path('project/<int:pk>', 
        views.ProjectDetailView.as_view(), 
        name='project-detail')
]
