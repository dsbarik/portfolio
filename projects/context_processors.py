from .models import Profile


def profile_context(request):
    """Add profile data to all templates"""
    return {"profile": Profile.get_profile()}
