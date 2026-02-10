from django.urls import path

from .views import ProjectDetailView, home

urlpatterns = [
    path("", home, name="home"),
    path("project/<slug:slug>/", ProjectDetailView.as_view(), name="project_detail"),
]
