from .models import UserProfile

def add_user_profile(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return {'user_profile': user_profile}