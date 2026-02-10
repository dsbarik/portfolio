from django.contrib import admin
from django.utils.html import format_html

from .models import Education, Experience, Profile, Project


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for managing personal profile/hero section.
    Only one profile should exist.
    """

    fieldsets = (
        (
            "Personal Information",
            {
                "fields": ("name", "title", "bio"),
            },
        ),
        (
            "Branding",
            {
                "fields": ("logo", "favicon"),
                "description": "Upload your logo and favicon. Logo appears in navbar, favicon in browser tab.",
            },
        ),
        (
            "Contact & Social Links",
            {
                "fields": (
                    "email",
                    "github_url",
                    "linkedin_url",
                    "kaggle_url",
                    "twitter_url",
                ),
                "description": "Add your social media and contact links. Leave blank if not applicable.",
            },
        ),
    )

    readonly_fields = ["updated_at"]

    def has_add_permission(self, request):
        # Only allow one profile to exist
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deleting the profile
        return False


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """
    Admin interface for managing work experience
    """

    list_display = ["position", "company", "duration_display", "order"]
    list_filter = ["is_current", "start_date"]
    search_fields = ["company", "position", "description"]
    list_editable = ["order"]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("company", "position", "location"),
            },
        ),
        (
            "Duration",
            {
                "fields": ("start_date", "end_date", "is_current"),
                "description": 'Set "Currently working here" to True if this is your current position.',
            },
        ),
        (
            "Description",
            {
                "fields": ("description",),
            },
        ),
        (
            "Display Settings",
            {
                "fields": ("order",),
            },
        ),
    )

    def duration_display(self, obj):
        """Display formatted duration in list view"""
        return obj.duration

    duration_display.short_description = "Duration"

    def get_form(self, request, obj=None, **kwargs):
        return form


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    """
    Admin interface for managing education
    """

    list_display = ["degree", "institution", "duration", "order"]
    list_filter = ["is_current", "start_date"]
    search_fields = ["institution", "degree"]
    list_editable = ["order"]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("institution", "degree", "location"),
            },
        ),
        (
            "Duration",
            {
                "fields": ("start_date", "end_date", "is_current"),
            },
        ),
        (
            "Details",
            {
                "fields": ("description", "order"),
            },
        ),
    )

    def duration(self, obj):
        return obj.duration

    duration.short_description = "Period"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Project model with enhanced features
    for managing dynamic fields.
    """

    list_display = ["title", "is_published", "order", "created_at", "image_preview"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_published", "order"]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "association",
                    "time_frame",
                    "role",
                    "featured_image",
                    "description",
                )
            },
        ),
        (
            "Custom Fields (JSON)",
            {
                "fields": ("custom_fields",),
                "description": """
                <p><strong>Add extra attributes as JSON.</strong> Use this for things that vary by project (technologies, links, gallery).</p>
                <p>Examples:</p>
                <pre style="background: #f5f5f5; padding: 10px; border-radius: 4px;">{
    "technologies": ["Python", "Django", "React"],
    "github_url": "https://github.com/...",
    "live_url": "https://example.com"
}</pre>
            """,
            },
        ),
        ("Publishing", {"fields": ("is_published", "order")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = ["created_at", "updated_at"]

    def image_preview(self, obj):
        """Display thumbnail of featured image in list view"""
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.featured_image.url,
            )
        return "-"

    image_preview.short_description = "Image"

    def get_form(self, request, obj=None, **kwargs):
        """Customize the form to make custom_fields more user-friendly"""
        form = super().get_form(request, obj, **kwargs)

        # Add help text for custom_fields
        if "custom_fields" in form.base_fields:
            form.base_fields["custom_fields"].widget.attrs.update({
                "rows": 15,
                "style": "font-family: monospace; width: 100%;",
            })

        # Add markdown support for description
        if "description" in form.base_fields:
            form.base_fields["description"].widget.attrs.update({
                "rows": 10,
                "style": "width: 100%;",
                "placeholder": """Markdown supported.
                
# Project Header
                
Description text...
                
- Feature 1
- Feature 2
""",
            })

        return form

    actions = ["publish_projects", "unpublish_projects"]

    def publish_projects(self, request, queryset):
        """Bulk action to publish selected projects"""
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} project(s) published successfully.")

    publish_projects.short_description = "Publish selected projects"

    def unpublish_projects(self, request, queryset):
        """Bulk action to unpublish selected projects"""
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} project(s) unpublished successfully.")

    unpublish_projects.short_description = "Unpublish selected projects"


# Customize admin site header
admin.site.site_header = "Portfolio Administration"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Management"
