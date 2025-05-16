from django.contrib import admin
from django.urls import path, include
from abcpet_app.views import dashboard
from django.conf import settings
from django.conf.urls.static import static
from abcpet_app import views
from django.contrib.auth import views as auth_views
from abcpet_app.views import login_step3 
from abcpet_app.views import login_step4  
from django.urls import path, include






urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('confirm-email-simple/<str:token>/', views.confirm_email_simple, name='confirm_email_simple'),


    path('admin/', admin.site.urls),
    path('', include('abcpet_app.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('login/step3/', login_step3, name='login_step3'),
    path('login/step4/', login_step4, name='login_step4'), 
       
] 

# Agregar las URLs estáticas y de medios solo si DEBUG es True
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)