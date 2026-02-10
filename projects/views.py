from django.shortcuts import render
from django.views.generic import DetailView

from .models import Education, Experience, Profile, Project


def home(request):
    """
    Homepage view displaying hero section, experiences, and projects
    """
    # Get the singleton profile (create default if not exists)
    profile = Profile.get_profile()

    # Get all projects
    projects = Project.objects.filter(is_published=True).order_by(
        "order", "-created_at"
    )

    # Get experiences
    experiences = Experience.objects.all()

    # Get education
    education = Education.objects.all()

    context = {
        "profile": profile,
        "projects": projects,
        "experiences": experiences,
        "education": education,
    }
    return render(request, "projects/home.html", context)


class ProjectDetailView(DetailView):
    """Display individual project details"""

    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        # Only show published projects
        return Project.objects.filter(is_published=True)
