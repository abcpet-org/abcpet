from .models import LoginDetail
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

class LoginDetailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            # Registra detalles de inicio de sesión
            LoginDetail.objects.create(
                user=request.user,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )

        return response
    
class AdminRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/administrador/') and not request.path.startswith('/administrador/login/'):
            if not request.user.is_authenticated:
                return redirect('/administrador/login/')
            if not request.user.is_staff:
                raise PermissionDenied("No tienes permiso para acceder a esta página.")
        response = self.get_response(request)
        return response