from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Profile(models.Model):
    """
    Singleton model for managing hero section/personal information.
    Only one profile should exist in the database.
    """

    name = models.CharField(max_length=200, help_text="Your full name")
    title = models.CharField(max_length=200, help_text="Your professional title/role")
    bio = models.TextField(help_text="Short bio/introduction (2-3 sentences)")

    # Branding
    logo = models.ImageField(
        upload_to="branding/",
        blank=True,
        null=True,
        help_text="Logo image for navbar (recommended: 200x50px PNG with transparent background)",
    )
    favicon = models.ImageField(
        upload_to="branding/",
        blank=True,
        null=True,
        help_text="Favicon for browser tab (recommended: 32x32px or 64x64px PNG/ICO)",
    )

    # Contact & Social Links
    email = models.EmailField(help_text="Contact email address")
    github_url = models.URLField(blank=True, help_text="GitHub profile URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    kaggle_url = models.URLField(blank=True, help_text="Kaggle profile URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter/X profile URL")

    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return f"Profile: {self.name}"

    def save(self, *args, **kwargs):
        # Ensure only one profile exists (singleton pattern)
        if not self.pk and Profile.objects.exists():
            # If trying to create a new profile when one exists, update the existing one
            existing = Profile.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

    @classmethod
    def get_profile(cls):
        """Get or create the profile instance"""
        profile, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                "name": "Your Name",
                "title": "Your Title",
                "bio": "Your bio here.",
                "email": "your.email@example.com",
            },
        )
        return profile


class Experience(models.Model):
    """
    Model for work experience/internships
    """

    company = models.CharField(max_length=200, help_text="Company/Organization name")
    position = models.CharField(max_length=200, help_text="Job title/position")
    location = models.CharField(
        max_length=200, blank=True, help_text="Location (optional)"
    )
    start_date = models.DateField(help_text="Start date")
    end_date = models.DateField(
        blank=True, null=True, help_text="End date (leave blank if current)"
    )
    is_current = models.BooleanField(default=False, help_text="Currently working here")
    description = models.TextField(
        help_text="Job description and responsibilities. Supports Markdown formatting for easy bullet points and paragraphs."
    )

    # Ordering
    order = models.IntegerField(
        default=0, help_text="Display order (lower numbers appear first)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-start_date"]
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"

    def __str__(self):
        return f"{self.position} at {self.company}"

    @property
    def duration(self):
        """Get formatted duration string"""
        start = self.start_date.strftime("%b %Y")
        if self.is_current:
            return f"{start} – Present"
        elif self.end_date:
            end = self.end_date.strftime("%b %Y")
            return f"{start} – {end}"
        return start


class Education(models.Model):
    """
    Model for education Details
    """

    institution = models.CharField(
        max_length=200, help_text="University/College/School name"
    )
    degree = models.CharField(max_length=200, help_text="Degree/Certificate name")
    location = models.CharField(
        max_length=200, blank=True, help_text="Location (optional)"
    )
    start_date = models.DateField(help_text="Start date")
    end_date = models.DateField(
        blank=True, null=True, help_text="End date (leave blank if current)"
    )
    is_current = models.BooleanField(default=False, help_text="Currently studying here")
    description = models.TextField(
        blank=True, help_text="Optional description. Supports Markdown."
    )

    # Ordering
    order = models.IntegerField(
        default=0, help_text="Display order (lower numbers appear first)"
    )

    class Meta:
        ordering = ["order", "-start_date"]
        verbose_name = "Education"
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} at {self.institution}"

    @property
    def duration(self):
        """Get formatted duration string"""
        start = self.start_date.strftime("%Y")
        if self.is_current:
            return f"{start} – Present"
        elif self.end_date:
            end = self.end_date.strftime("%Y")
            return f"{start} – {end}"
        return start


class Project(models.Model):
    """
    Dynamic project model with flexible attributes stored in JSON.

    Base fields provide core functionality, while custom_fields allows
    storing any additional project-specific data without schema changes.
    """

    # Core fields
    title = models.CharField(max_length=200, help_text="Project title")
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        help_text="URL-friendly version of title (auto-generated)",
    )
    description = models.TextField(
        help_text="Main project description. Supports Markdown formatting."
    )

    # Key Details
    association = models.CharField(
        max_length=200,
        blank=True,
        help_text="Client, Company, or Organization associated with this project",
    )
    time_frame = models.CharField(
        max_length=100,
        blank=True,
        help_text="Duration or period (e.g., 'Jan 2023 - Present', '3 months')",
    )
    role = models.CharField(
        max_length=200,
        blank=True,
        help_text="Your role in the project (e.g., 'Lead Developer', 'Researcher')",
    )

    # Image
    featured_image = models.ImageField(
        upload_to="projects/", blank=True, null=True, help_text="Main project image"
    )

    # Dynamic fields - stores flexible key-value pairs
    custom_fields = models.JSONField(
        default=dict,
        blank=True,
        help_text="Custom project attributes (technologies, links, galleries, etc.)",
    )

    # Publishing
    is_published = models.BooleanField(
        default=False, help_text="Whether this project is visible on the site"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Ordering
    order = models.IntegerField(
        default=0, help_text="Display order (lower numbers appear first)"
    )

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})

    def get_custom_field(self, key, default=None):
        """Helper method to safely get custom field values"""
        return self.custom_fields.get(key, default)

    def set_custom_field(self, key, value):
        """Helper method to set custom field values"""
        self.custom_fields[key] = value
