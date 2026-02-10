from django_distill import distill_path

from .models import Project
from .views import ProjectDetailView, home


def get_project_slugs():
    for project in Project.objects.all():
        yield {"slug": project.slug}


urlpatterns = [
    distill_path("", home, name="home"),
    distill_path(
        "project/<slug:slug>/",
        ProjectDetailView.as_view(),
        name="project_detail",
        distill_func=get_project_slugs,
    ),
]
