from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectsListView.as_view(), name='index')
]

# urlpatterns = [
#     path('', views.ProjectsListView.as_view(), name='index'),
#     path('/<str:category>', CategoryListView.as_view(), name='category-view'),
#     path('/<str:technology>', TechnologyListView.as_view(), name='technology-view'),
#     path('/<int:id>', ProjectDetailView.as_view(), name='detail-view')
# ]
