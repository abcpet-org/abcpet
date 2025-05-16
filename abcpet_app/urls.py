from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    # Vistas de autenticación y perfil
    signup, login_view, logout_view, CustomLoginView,
    login_step1, login_step2, login_step3, login_step4, login_step5,
    resend_otp, resend_confirmation_email, confirm_email,
    email_confirmed, email_confirm_invalid,

    # Vistas de dashboard y perfil de usuario
    index, dashboard, dashboard_view, edit_profile, mi_perfil,
    user_payment, user_wallet, save_profile_field, login_history,
    privacy_settings,

    # Vistas de mascotas
    detalle_mascota, crear_mascota, MascotaDetailView, obtener_razas,
    mascota_dashboard, editar_mascota, detalle_mascota_edit,

    # Vistas de anfitriones/proveedores
    register_host_view, approve_host_view, success_page, approve_individual_host_view,
    register_host1, register_host2, provider_profile, host_view,
    search_hosts, resultados_busqueda, detalle_host, get_updated_body,

    # Vistas de administración
    admin_login, admin_dashboard, admin_logout, admin_dashboard_view,
    user_management_view, site_settings_view, edit_user_view, add_new_item,

    # Vistas de recuperación de contraseña
    send_reset_code, verify_code, change_password, password_changed
)

# Configuración del router para API REST
router = DefaultRouter()
router.register(r'userprofile', views.UserProfileViewSet)

urlpatterns = [
    # Páginas principales
    path('', index, name='index'),
    
    # Autenticación y registro
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Flujo de registro paso a paso
    path('login/step1/', views.login_step1, name='login_step1'),
    path('login/step2/', views.login_step2, name='login_step2'),
    path('login/step3/', login_step3, name='login_step3'),
    path('login/step4/', login_step4, name='login_step4'),
    path('login/step5/', login_step5, name='login_step5'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    
    # Confirmación de correo electrónico
    path('resend_confirmation_email/', views.resend_confirmation_email, name='resend_confirmation_email'),
    path('email-confirmed/', views.email_confirmed, name='email_confirmed'),
    path('email-confirm-invalid/', views.email_confirm_invalid, name='email_confirm_invalid'),
    path('confirm-email/<str:token>/', views.confirm_email, name='confirm_email'),
    
    # Dashboard y perfil de usuario
    path('dashboard/', dashboard, name='dashboard'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('mi_perfil/', mi_perfil, name='mi_perfil'),
    path('user_payment/', user_payment, name='user_payment'),
    path('user_wallet/', user_wallet, name='user_wallet'),
    path('save_profile_field/', save_profile_field, name='save_profile_field'),
    path('login_history/', login_history, name='login_history'),
    path('privacy_settings/', privacy_settings, name='privacy_settings'),
    
    # Gestión de mascotas
    path('crear_mascota/', crear_mascota, name='crear_mascota'),
    path('detalle_mascota/<int:mascota_id>/', detalle_mascota, name='detalle_mascota'),
    path('detalle_mascota/', MascotaDetailView.as_view(), name='detalle_mascota'),
    path('editar_mascota/', views.editar_mascota, name='editar_mascota'),
    path('detalle_mascota_edit/', views.detalle_mascota_edit, name='detalle_mascota_edit'),
    path('obtener_razas/', obtener_razas, name='obtener_razas'),
    path('dashboard/mascota-dashboard/<int:mascota_id>/<str:nombre_mascota>/', views.mascota_dashboard, name='mascota_dashboard'),
    
    # API y endpoints
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/search-hosts/', views.search_hosts, name='search-hosts'),
    
    # Gestión de anfitriones/proveedores
    path('register_host/', register_host_view, name='register_host'),
    path('register_host1/', register_host1, name='register_host1'),
    path('register_host2/', views.register_host2, name='register_host2'),
    path('approve_host/', approve_host_view, name='approve_host'),
    path('approve_host/<int:host_id>/', approve_host_view, name='approve_host'),
    path('approve_host/approve/<int:host_id>/', approve_individual_host_view, name='approve_individual_host'),
    path('success/', success_page, name='success_page'),
    path('provider-profile/', views.provider_profile, name='provider_profile'),
    path('provider_profile', views.provider_profile, name='provider_profile'),
    path('host/', views.host_view, name='host'),
    path('resultados_busqueda', views.resultados_busqueda, name='resultados_busqueda'),
    re_path(r'^resultados_busqueda/$', views.resultados_busqueda, name='resultados_busqueda'),
    path('detalle_host/<int:anfitrion_id>/', views.detalle_host, name='detalle_host'),
    path('get-updated-body/', get_updated_body, name='get-updated-body'),
    
    # Gestión de contraseñas
    path('change_password/', change_password, name='change_password'),
    path('change_password/<int:user_id>/', change_password, name='change_password'),
    path('send_reset_code/', send_reset_code, name='send_reset_code'),
    path('verify_code/', verify_code, name='verify_code'),
    path('password_changed/', password_changed, name='password_changed'),
    
    # Rutas de restablecimiento de contraseña de Django
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset_password_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), name="password_reset_complete"),
    
    # Administración
    path('administrador/login/', admin_login, name='admin_login'),
    path('administrador/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('administrador/logout/', admin_logout, name='admin_logout'),
    path('user-management/', views.user_management_view, name='user_management'),
    path('site-settings/', views.site_settings_view, name='site_settings'),
    path('edit-user/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('add_new_item/', views.add_new_item, name='add_new_item'),
    
    # Alias y redirecciones
    path('url1/', views.dashboard, name='url1'),
]