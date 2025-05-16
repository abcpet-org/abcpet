import re
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render
from .forms import EditProfileForm
from .models import UserProfile

from .forms import UserPaymentForm
from .models import UserPayment 
from django.urls import reverse
from django.contrib import messages
from .forms import PromoCodeForm
from .models import UserWallet
from decimal import Decimal
from django.http import JsonResponse
from django.http import Http404
from django.http import JsonResponse, Http404
from .forms import EditProfileForm
from .models import LoginDetail
from .forms import PrivacySettingsForm
from .forms import MascotaForm
from django.shortcuts import render, get_object_or_404
from .models import Mascota
from django.shortcuts import render, HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import MascotaFoto
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import UserProfileSerializer
from .permissions import IsSuperUser
from .forms import ABCPetHostForm
from .models import ABCPetHost
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import ABCPetHost
from .forms import ABCPetHostForm 
from .forms import CustomLoginForm
from django.contrib.auth.views import LoginView
from .forms import CustomUserEditForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from abcpet_app.models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import CustomUser
from .forms import CustomUserCreationForm  # Asegúrate de importar tu formulario de registro personalizado
from django.views.decorators.cache import never_cache
import logging
from .forms import CustomUserCreationForm  
from .forms import CustomUserStep4Form
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
import requests
from .models import EmailConfirmationToken
from .utils import send_confirmation_email
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta  
from .models import EmailConfirmationToken  # Asegúrate de importar tu modelo de token
from django.core.mail import send_mail
from .models import ABCPetHost
from .forms import ABCPetHostForm1
from .models import UserProfile
from .forms import ABCPetHostForm2
import os
from .forms import UserPaymentForm
from .models import UserPayment
from .forms import UserPaymentForm
from django import forms
from decimal import Decimal
from django.contrib import messages
from .models import UserWallet, UserPayment
from .forms import PromoCodeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomPasswordChangeForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import CustomUser  # Asegúrate de importar tu modelo de usuario personalizado
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import CustomUser 
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from .models import PasswordResetCode
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .models import PasswordResetCode, CustomUser  # Importa tu modelo de usuario personalizado
from .forms import UserForm  # Asegúrate de que esta línea esté presente


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .utils import send_otp_email
from django.contrib.auth import get_user_model




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache
import random
from .models import OTPCode  






User = get_user_model() 





class UserPaymentForm(forms.ModelForm):
    class Meta:
        model = UserPayment
        fields = ['card_number', 'cvc', 'expiration_date', 'card_type']
        widgets = {
            'card_number': forms.PasswordInput(),
            'cvc': forms.PasswordInput(),
        }









class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'abcpet_app/login.html'  # Asegúrate de que esta plantilla exista




# Vista para editar el perfil fsfsfdfdf
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = CustomUserEditForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            print(profile_form.cleaned_data.get('rut'))  # Añade este print para verificar el valor del campo RUT
            profile_form.save()
            return redirect('dashboard')  # O cualquier URL a la que quieras redirigir después del guardado

    else:
        user_form = CustomUserEditForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.userprofile)
        
        # Imprimir valores para depuración
        print("Calle Numero:", request.user.userprofile.calle_numero)
        print("Info Adicional:", request.user.userprofile.info_adicional)
        print("Country:", request.user.userprofile.country)
        
        
        initial_values = {}
        if request.user.userprofile.calle_numero is None:
            initial_values['calle_numero'] = ''
        if request.user.userprofile.info_adicional is None:
            initial_values['info_adicional'] = ''
        if request.user.userprofile.country is None:
            initial_values['country'] = ''

        if initial_values:
            profile_form = EditProfileForm(instance=request.user.userprofile, initial=initial_values)
        
    

    return render(request, 'abcpet_app/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Desactivar la cuenta hasta que el email sea confirmado
            user.save()

            # Enviar email de confirmación
            send_confirmation_email(user)

            # Redirigir a una página que indique al usuario verificar su email
            return redirect('email_confirmation_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'abcpet_app/signup.html', {'form': form})

    

def index(request):
    # Obtener todos los usuarios aprobados
    usuarios_aprobados = ABCPetHost.objects.filter(aprobado=True)

    context = {
        'aprobados': usuarios_aprobados,
    }

    return render(request, 'abcpet_app/index.html', context)

@never_cache
def login_view(request):
    """
    Vista para el inicio de sesión
    """
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me', False)
        
        # Validación básica
        if not email or not password:
            messages.error(request, "Por favor ingresa tu correo y contraseña.")
            return render(request, 'abcpet_app/login.html')
        
        # Intentar autenticar al usuario
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Verificar si el usuario está activo
            if user.is_active:
                # Iniciar sesión
                login(request, user)
                
                # Configurar la expiración de la sesión según la opción de "recordarme"
                if not remember_me:
                    # Si no marca "recordarme", la sesión expira al cerrar el navegador
                    request.session.set_expiry(0)
                else:
                    # Si marca "recordarme", la sesión dura 2 semanas
                    request.session.set_expiry(1209600)  # 2 semanas en segundos
                
                # Registrar el inicio de sesión (opcional)
                # LoginHistory.objects.create(user=user, ip_address=get_client_ip(request))
                
                # Redirigir al dashboard
                return redirect('dashboard')
            else:
                messages.error(request, "Tu cuenta no está activa. Por favor verifica tu correo electrónico.")
                return render(request, 'abcpet_app/login.html')
        else:
            messages.error(request, "Correo electrónico o contraseña incorrectos.")
            return render(request, 'abcpet_app/login.html')
    
    return render(request, 'abcpet_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')




@login_required
def dashboard(request):
    """
    Vista del dashboard principal con todas las estadísticas y datos relevantes del usuario
    """
    # Obtener las mascotas del usuario actual
    mascotas = Mascota.objects.filter(user=request.user)
    
    # Contar elementos relevantes para mostrar en el dashboard
    mascotas_count = mascotas.count()
    
    # Obtener las reservas activas del usuario (si existe un modelo para esto)
    # Puedes adaptar esto a tu modelo específico
    reservas_count = 0  # Por defecto sin reservas
    
    # Si tienes un modelo de Reserva, descomenta y adapta el siguiente código:
    # try:
    #     reservas_count = Reserva.objects.filter(user=request.user, estado='activa').count()
    # except:
    #     reservas_count = 0
    
    # Calcular calificación promedio (si tienes un modelo para esto)
    calificacion_promedio = 0.0  # Por defecto sin calificaciones
    
    # Si tienes un modelo de calificaciones, descomenta y adapta:
    # from django.db.models import Avg
    # try:
    #     calificacion_promedio = Calificacion.objects.filter(
    #         user=request.user
    #     ).aggregate(Avg('puntuacion'))['puntuacion__avg'] or 0.0
    # except:
    #     calificacion_promedio = 0.0
    
    # Obtener créditos disponibles
    creditos = 0  # Por defecto sin créditos
    
    try:
        creditos = UserWallet.objects.get(user=request.user).balance
    except UserWallet.DoesNotExist:
        creditos = 0
    
    # Obtener actividad reciente (si existe un modelo para esto)
    # Si tienes un modelo de Actividad, descomenta y adapta:
    # try:
    #     actividad_reciente = Actividad.objects.filter(user=request.user).order_by('-fecha')[:5]
    # except:
    #     actividad_reciente = []
    
    # Obtener notificaciones (si existe un modelo para esto)
    # Si tienes un modelo de Notificaciones, descomenta y adapta:
    # try:
    #     notifications = Notificacion.objects.filter(user=request.user, leida=False)
    #     notifications_count = notifications.count()
    # except:
    #     notifications_count = 0
    
    context = {
        'mascotas': mascotas,
        'mascotas_count': mascotas_count,
        'reservas_count': reservas_count,
        'calificacion_promedio': calificacion_promedio,
        'creditos': creditos,
        'actividad_reciente': [],  # Lista vacía por defecto o actividad_reciente si lo has implementado
        'proximas_reservas': [],   # Lista vacía por defecto o próximas reservas si lo has implementado
        'notifications_count': 0,  # O notifications_count si lo has implementado
        'mensajes_count': 0,       # O mensajes_count si lo has implementado
    }
    
    return render(request, 'abcpet_app/dashboard.html', context)




def mi_perfil(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'abcpet_app/mi_perfil.html', {'user_profile': user_profile})



def agregar_tarjeta(request):
    if request.method == 'POST':
        form = UserPaymentForm(request.POST)
        if form.is_valid():
            # Crea una instancia del modelo UserPayment con los datos del formulario
            user_payment = form.save(commit=False)
            # Asigna el usuario actual a la instancia de UserPayment
            user_payment.user = request.user
            user_payment.save()
            # Redirecciona a alguna página de éxito o muestra un mensaje de éxito
            return redirect('dashboard')  # Redirecciona al dashboard u otra página
    else:
        form = UserPaymentForm()
    return render(request, 'agregar_tarjeta.html', {'form': form})



@login_required
def user_payment(request):
    if request.method == 'POST':
        form = UserPaymentForm(request.POST)
        if form.is_valid():
            user_payment = form.save(commit=False)
            user_payment.user = request.user
            user_payment.save()
            return redirect('dashboard')  # Redirige a donde desees después de guardar la tarjeta
    else:
        form = UserPaymentForm()
    return render(request, 'dashboard/user_payment.html', {'form': form})
import re


def determine_card_type(card_number):
    # Utiliza un patrón para determinar el tipo de tarjeta
    visa_pattern = re.compile(r'^4[0-9]{12}(?:[0-9]{3})?$')
    mastercard_pattern = re.compile(r'^5[1-5][0-9]{14}$')

    if visa_pattern.match(card_number):
        return 'Visa'
    elif mastercard_pattern.match(card_number):
        return 'Mastercard'
    else:
        return 'Desconocido'



def user_wallet(request):
    try:
        wallet = UserWallet.objects.get(user=request.user)
    except UserWallet.DoesNotExist:
        # Crea una billetera para el usuario si no existe
        wallet = UserWallet.objects.create(user=request.user)

    promo_form = None  # Definir promo_form antes de la lógica condicional

    if request.method == 'POST':
        promo_form = PromoCodeForm(request.POST)
        if promo_form.is_valid():
            promo_code = promo_form.cleaned_data['promo_code']
            if promo_code == 'ABCPET':
                # Convertir el valor a Decimal antes de sumar
                wallet.balance += Decimal('5000.00')
                wallet.promo_used = True  # Marcar el código como utilizado
                wallet.save()
                messages.success(request, 'Código promocional aplicado con éxito. Se han añadido $5000 CLP a tu billetera.')
            else:
                messages.error(request, 'Código promocional no válido.')
    elif request.method == 'GET':
        promo_form = PromoCodeForm()  # Asignar el valor en caso de solicitud GET

    # Obtener detalles de la tarjeta del usuario
    try:
        user_payment = UserPayment.objects.get(user=request.user)
    except UserPayment.DoesNotExist:
        user_payment = None

    context = {
        'wallet': wallet,
        'promo_form': promo_form,
        'user_payment': user_payment,
        
    }

    print(user_payment)  # Añade esta línea para depuración

    return render(request, 'dashboard/user_wallet.html', context)



def save_profile_field(request):
    try:
        if request.method == 'POST':
            field = request.POST.get('field')
            value = request.POST.get('value')
            print(f'Received data - Field: {field}, Value: {value}')

            # Validar que el campo exista en el modelo User o UserProfile
            user_fields = [field.name for field in User._meta.get_fields()]
            user_profile_fields = [field.name for field in UserProfile._meta.get_fields()]

            if field in user_fields:
                user = User.objects.get(pk=request.user.pk)

                if field == 'first_name':
                    user.first_name = value
                elif field == 'last_name':
                    user.last_name = value
                elif field == 'username':
                    user.username = value
                elif field == 'email':
                    print(f'Updating email for user: {request.user.username} - New email: {value}')
                    user.email = value
                    user.save()
                else:
                    # Si hay otros campos en el modelo User, agrégales aquí
                    raise Http404(f'Campo {field} no manejado en esta vista')

                user.save()

            elif field in user_profile_fields:
                user_profile = UserProfile.objects.get(user=request.user)

                if field == 'phone_number':
                    user_profile.phone_number = value
                
                else:
                    # Si hay otros campos en el modelo UserProfile, agrégales aquí
                    raise Http404(f'Campo {field} no manejado en esta vista')

                user_profile.save()

            else:
                raise Http404(f'Campo {field} no encontrado en los modelos User ni UserProfile')

            return JsonResponse({'success': True})

        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method'})

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User no encontrado para este usuario'})
    except UserProfile.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'UserProfile no encontrado para este usuario'})
    except Http404 as e:
        print(f'Error 404: {e}')
        return JsonResponse({'success': False, 'message': str(e)})
    except Exception as e:
        print(f'Error inesperado: {e}')
        return JsonResponse({'success': False, 'message': str(e)})
    
    
      
@login_required
def login_history(request):
    login_details = LoginDetail.get_login_details(request.user)
    user_management_view = request.user.is_superuser
    user_wallet_view = request.user.is_superuser
    user_payment= request.user.is_superuser
    return render(request, 'dashboard/login_history.html', {'login_details': login_details})



def privacy_settings(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = PrivacySettingsForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            # Puedes agregar un mensaje de éxito si lo deseas
            return redirect('privacy_settings')
    else:
        form = PrivacySettingsForm(instance=user_profile)

    context = {
        'form': form,
    }

    return render(request, 'dashboard/privacy_settings.html', context)



@login_required
def crear_mascota(request):
    usuario = request.user

    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.user = request.user  # Asocia la mascota con el usuario actual
            if not mascota.consume_medicacion:
                mascota.detalles_medicacion = "No aplica polli"
            mascota.save()
            for uploaded_file in request.FILES.getlist('galeria_fotos'):
                mascota_foto = MascotaFoto(mascota=mascota, imagen=uploaded_file)
                mascota_foto.save()

            return redirect('dashboard')
    else:
        # Puedes usar el formulario sin la necesidad de inicializar el campo 'user'
        form = MascotaForm()

    return render(request, 'dashboard/crear_mascota.html', {'form': form})



@login_required
def detalle_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, pk=mascota_id, user=request.user)
    fotos_mascota = MascotaFoto.objects.filter(mascota=mascota)

    context = {'mascota': mascota, 'fotos_mascota': fotos_mascota}
    return render(request, 'dashboard/detalle_mascota.html', context)



class MascotaDetailView(LoginRequiredMixin, ListView):
    model = Mascota
    template_name = 'dashboard/detalle_mascota.html'
    context_object_name = 'mascotas'

    def get_queryset(self):
        # Filtra las mascotas asociadas al usuario actual
        return Mascota.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        mascotas = self.get_queryset()

        if not mascotas.exists():
            # Si no hay mascotas, redirige a la vista de creación de mascotas
            return redirect('crear_mascota')

        return super().get(request, *args, **kwargs)
    
  
    
def editar_mascota(request):
    # Lógica para editar la mascota
    return render(request, 'dashboard/editar_mascota.html', {})



def detalle_mascota_edit(request):
    return render(request, 'dashboard/detalle_mascota_edit.html')



def obtener_razas(request):
    tipo_mascota = request.GET.get('tipo_mascota', None)
    razas = Mascota.get_razas_por_tipo(tipo_mascota)
    return JsonResponse({'razas': razas})



def mascota_dashboard(request, mascota_id, nombre_mascota):
    mascota = get_object_or_404(Mascota, pk=mascota_id, nombre_mascota=nombre_mascota)
    return render(request, 'dashboard/mascota-dashboard.html', {'mascota': mascota})



def detalle_mascota(request):
    # Aquí puedes agregar cualquier lógica necesaria para obtener los datos de las mascotas
    return render(request, 'detalle_mascota.html')



class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    
    
@login_required
def register_host(request):
    if request.method == 'POST':
        form = ABCPetHostForm(request.POST, request.FILES)
        if form.is_valid():
            host = form.save(commit=False)
            host.user = request.user  # Asignar el usuario actual
            host.save()
            return redirect('dashboard/success')  # reemplaza 'success_url' con la URL a la que deseas redirigir después de un envío exitoso
    else:
        form = ABCPetHostForm()
    return render(request, 'dashboard/register_host.html', {'form': form})



@login_required
def register_host_view(request):
    user = request.user

    # Verifica si el usuario ya tiene un registro ABCPetHost
    if ABCPetHost.objects.filter(user=user).exists():
        return redirect('provider_profile')  # Redirige al usuario a la página de perfil del proveedor

    # Maneja la creación de un nuevo registro ABCPetHost
    if request.method == 'POST':
        print("Formulario recibido")  # Depuración: Confirma que el formulario fue recibido
        form = ABCPetHostForm(request.POST, request.FILES)
        if form.is_valid():
            print("Formulario válido")  # Depuración: El formulario es válido
            host = form.save(commit=False)
            host.user = request.user
            host.save()
            return redirect('provider_profile')  # Redirige a la página de perfil del proveedor
        else:
            print("Formulario inválido")  # Depuración: El formulario es inválido
            print(form.errors)  # Imprime los errores del formulario
    else:
        form = ABCPetHostForm()

    return render(request, 'dashboard/register_host.html', {'form': form})



@login_required
def approve_host_view(request):
    # Suponiendo que solo los superusuarios pueden ver y aprobar
    if not request.user.is_superuser:
        # Manejar el caso en que el usuario no tenga permiso
        return render(request, 'sin_permiso.html')

    # Obtener todas las solicitudes de anfitrión no aprobadas
    pending_hosts = ABCPetHost.objects.filter(aprobado=False)

    return render(request, 'dashboard/approve_host_list.html', {'pending_hosts': pending_hosts})



@login_required
def approve_individual_host_view(request, host_id):
    if not request.user.is_superuser:
        # Manejar el caso en que el usuario no tenga permiso
        return render(request, 'sin_permiso.html')

    host_application = get_object_or_404(ABCPetHost, id=host_id)
    host_application.aprobado = True
    host_application.save()

    # Redirigir de vuelta a la lista de solicitudes pendientes
    return redirect('dashboard/approve_host')

def success_page(request):
    return render(request, 'dashboard/success_page.html')
    
 
    
@login_required
def provider_profile(request):
    user = request.user

    # Verificación para el perfil del proveedor
    is_profile_complete = all([
        user.first_name.strip() and user.first_name.strip().lower() != "no proporcionado",
        user.last_name.strip() and user.last_name.strip().lower() != "no proporcionado",
        user.email.strip() and user.email.strip().lower() != "no proporcionado",
        # Continúa con otros campos necesarios para el perfil del proveedor
    ])

    # Verificación para la configuración de embarque de mascotas 
    try:
        abcpet_host = ABCPetHost.objects.get(user=user)
        is_pet_shipment_config_complete = abcpet_host.is_config_complete()
    except ABCPetHost.DoesNotExist:
        is_pet_shipment_config_complete = False

    context = {
        'is_profile_complete': is_profile_complete,
        'is_pet_shipment_config_complete': is_pet_shipment_config_complete
    }

    return render(request, 'dashboard/provider_profile.html', context)



@login_required
def get_updated_body(request):
    user = request.user

    # Verificación para el perfil del proveedor
    is_profile_complete = all([
        user.first_name.strip() and user.first_name.strip().lower() != "no proporcionado",
        user.last_name.strip() and user.last_name.strip().lower() != "no proporcionado",
        user.email.strip() and user.email.strip().lower() != "no proporcionado",
        # Continúa con otros campos necesarios para el perfil del proveedor
    ])

    # Verificación para la configuración de embarque de mascotas
    try:
        abcpet_host = ABCPetHost.objects.get(user=user)
        is_pet_shipment_config_complete = abcpet_host.is_config_complete()
    except ABCPetHost.DoesNotExist:
        is_pet_shipment_config_complete = False

    # Renderizar solo las partes necesarias del HTML
    profile_config_html = render_to_string('dashboard/partials/profile_config_status.html', {
        'is_profile_complete': is_profile_complete
    })
    pet_shipment_config_html = render_to_string('dashboard/partials/pet_shipment_config_status.html', {
        'is_pet_shipment_config_complete': is_pet_shipment_config_complete
    })

    return JsonResponse({
        'profile_config_html': profile_config_html,
        'pet_shipment_config_html': pet_shipment_config_html
    })


@login_required
@csrf_exempt
def update_user_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_profile = request.user.userprofile

            # Logs para depuración
            print("Datos recibidos:", data)
            print("Perfil antes de actualizar:", user_profile.rut, user_profile.genero)

            # Actualización de datos
            request.user.first_name = data.get('first_name', request.user.first_name)
            request.user.last_name = data.get('last_name', request.user.last_name)
            if 'rut' in data:
                user_profile.rut = data['rut']
            if 'genero' in data:
                user_profile.genero = data['genero']
            if 'phone_number' in data:
                user_profile.phone_number = data['phone_number']
            if 'fecha_nacimiento' in data:
                user_profile.fecha_nacimiento = data['fecha_nacimiento']
            if 'newsletter_email' in data:
                user_profile.newsletter_email = data['newsletter_email']
            if 'newsletter_telefono' in data:
                user_profile.newsletter_telefono = data['newsletter_telefono']
            if 'country' in data:
                user_profile.country = data['country']
            if 'region' in data:
                user_profile.region = data['region']
            if 'comuna' in data:
                user_profile.comuna = data['comuna']
            if 'calle_numero' in data:
                user_profile.calle_numero = data['calle_numero']
            if 'info_adicional' in data:
                user_profile.info_adicional = data['info_adicional']
            if 'user_name' in data:
                user_profile.user_name = data['user_name']
                
                
           

            request.user.save()
            user_profile.save()
            
            

            # Log después de guardar
            print("Perfil actualizado:", user_profile.rut, user_profile.genero)

            return JsonResponse({'success': True})
        
        except Exception as e:
            print("Error:", e)  # Log del error
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


@login_required
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile_picture = request.FILES['profile_picture']

        # Validar que el archivo sea una imagen válida
        try:
            validate_image(profile_picture)
        except ValidationError:
            return JsonResponse({'success': False, 'error': 'El archivo no es una imagen válida'}, status=400)

        user_profile = request.user.userprofile
        user_profile.profile_picture = profile_picture

        # Guardar la imagen utilizando el método save() del campo ImageField
        try:
            user_profile.save()
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

        # Manejar correctamente el caso en el que se guarde correctamente la imagen
        response_data = {'success': True}
        return JsonResponse(response_data)

    # Manejar el caso en el que no se haya proporcionado ninguna imagen para cargar
    response_data = {'success': False, 'error': 'No se proporcionó ninguna imagen para cargar'}
    return JsonResponse(response_data, status=400)

def validate_image(image):
    # Validar que el archivo sea una imagen
    if not image.content_type.startswith('image'):
        raise ValidationError('El archivo no es una imagen')
    # Puedes agregar más validaciones aquí, como verificar el tamaño de la imagen



def verificar_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': CustomUser.objects.filter(email=email).exists()
    }
    return JsonResponse(data)



@never_cache
def login_step1(request):
    """
    Paso 1: Solicitar correo electrónico
    """
    # Limpiar datos de sesión anteriores al iniciar
    for key in list(request.session.keys()):
        if key not in ['_auth_user_id', '_auth_user_backend', '_auth_user_hash']:
            if key.startswith('user_'):
                del request.session[key]
    
    if request.method == 'POST':
        email = request.POST.get('email', '')
        
        if not email or '@' not in email or '.' not in email:
            messages.error(request, "Por favor ingresa un correo electrónico válido.")
            return render(request, 'abcpet_app/login_step1.html')
        
        # Verificar si el correo ya existe
        if User.objects.filter(email=email).exists():
            messages.error(request, "Este correo ya está registrado. Por favor inicia sesión.")
            return redirect('login')
        
        # Guardar en sesión
        request.session['user_email'] = email
        request.session.modified = True
        
        # Continuar al paso 2
        return redirect('login_step2')
    
    return render(request, 'abcpet_app/login_step1.html')

@never_cache
def login_step2(request):
    """
    Paso 2: Confirmación del correo
    """
    email = request.session.get('user_email')
    
    if not email:
        messages.error(request, "Información incompleta. Por favor inicia el registro nuevamente.")
        return redirect('login_step1')
    
    if request.method == 'POST':
        # Simplemente confirmamos y avanzamos
        return redirect('login_step3')
    
    return render(request, 'abcpet_app/login_step2.html', {'email': email})

@never_cache
def login_step3(request):
    """
    Paso 3: Creación de contraseña
    """
    email = request.session.get('user_email')
    
    if not email:
        messages.error(request, "Información incompleta. Por favor inicia el registro nuevamente.")
        return redirect('login_step1')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password', '')
        
        if not password or len(password) < 8:
            messages.error(request, "La contraseña debe tener al menos 8 caracteres.")
            return render(request, 'abcpet_app/login_step3.html')
        
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'abcpet_app/login_step3.html')
        
        # Guardar en sesión
        request.session['user_password'] = password
        request.session.modified = True
        
        # Continuar al paso 4
        return redirect('login_step4')
    
    return render(request, 'abcpet_app/login_step3.html')

@never_cache
def login_step4(request):
    """
    Paso 4: Datos personales
    """
    # Verificar datos necesarios
    email = request.session.get('user_email')
    password = request.session.get('user_password')
    
    if not email or not password:
        messages.error(request, "Información incompleta. Por favor inicia el registro nuevamente.")
        return redirect('login_step1')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        if not first_name or not last_name:
            messages.error(request, "Por favor completa tu nombre y apellido.")
            return render(request, 'abcpet_app/login_step4.html')
        
        # Crear usuario (inactivo)
        try:
            # Eliminar usuarios inactivos con el mismo email para evitar el error UNIQUE
            User = get_user_model()
            User.objects.filter(email=email, is_active=False).delete()
            
            # Crear nuevo usuario
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=False
            )
            
            # Guardar ID en sesión
            request.session['user_id'] = user.id
            
            # Enviar código OTP
            send_otp_email(user)
            
            # Continuar al paso 5
            return redirect('login_step5')
            
        except Exception as e:
            messages.error(request, f"Error al crear la cuenta: {str(e)}")
            print(f"ERROR DETALLADO: {e}")
    
    return render(request, 'abcpet_app/login_step4.html')

@never_cache
def login_step5(request):
    """
    Paso 5: Verificación OTP
    """
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, "No se encontraron datos de registro. Por favor comienza de nuevo.")
        return redirect('login_step1')
    
    try:
        user = User.objects.get(id=user_id)
        
        # Verificar OTP válido
        valid_otp = OTPCode.objects.filter(
            user=user, 
            is_used=False, 
            expires_at__gt=timezone.now()
        ).exists()
        
        if not valid_otp:
            tiempo_restante = 0
        else:
            otp = OTPCode.objects.filter(
                user=user,
                is_used=False,
                expires_at__gt=timezone.now()
            ).latest('created_at')
            tiempo_restante = max(0, (otp.expires_at - timezone.now()).total_seconds())
        
        if request.method == 'POST':
            entered_code = request.POST.get('otp_code', '')
            
            try:
                otp = OTPCode.objects.filter(
                    user=user, 
                    is_used=False,
                    expires_at__gt=timezone.now()
                ).latest('created_at')
                
                if otp.code == entered_code:
                    # Activar usuario
                    user.is_active = True
                    user.save()
                    
                    # Marcar OTP como usado
                    otp.is_used = True
                    otp.save()
                    
                    # Limpiar sesión
                    for key in ['user_email', 'user_password', 'user_id']:
                        if key in request.session:
                            del request.session[key]
                    
                    messages.success(request, "¡Tu cuenta ha sido verificada exitosamente!")
                    return redirect('email_confirmed')
                else:
                    messages.error(request, "Código incorrecto. Intenta nuevamente.")
            except OTPCode.DoesNotExist:
                messages.error(request, "El código ha expirado. Solicita uno nuevo.")
        
        context = {'tiempo_restante': int(tiempo_restante)}
        return render(request, 'abcpet_app/login_step5.html', context)
        
    except User.DoesNotExist:
        messages.error(request, "Usuario no encontrado. Por favor inicia el registro de nuevo.")
        return redirect('login_step1')


@never_cache
def resend_otp(request):
    """
    Reenviar código OTP
    """
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, "No se encontraron datos de registro.")
        return redirect('login_step1')
    
    try:
        user = User.objects.get(id=user_id)
        # Generar y enviar nuevo OTP
        send_otp_email(user)
        messages.success(request, "Se ha enviado un nuevo código a tu correo.")
    except User.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('login_step1')
    
    return redirect('login_step5')


def get_next_correlative():
    # Obtener el último número correlativo de los usuarios
    last_correlative = CustomUser.objects.order_by('-id').values_list('username', flat=True).first()

    if last_correlative:
        parts = last_correlative.split('/USR-')
        if len(parts) == 2 and parts[1].isdigit():
            return int(parts[1]) + 1

    # Si no se encontró un correlativo anterior, comienza desde 1
    return 1


def validate_recaptcha(response_token):
    secret_key = "6Ld080gpAAAAALF5H0epPFoa-PKZ_iWslcTUE-zc"
    recaptcha_response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={'secret': secret_key, 'response': response_token}
    )
    return recaptcha_response.json()



# En views.py
def confirm_email(request, token):
    from django.http import HttpResponse
    import traceback
    
    try:
        # Intenta encontrar el token
        confirmation = EmailConfirmationToken.objects.get(token=token)
        
        # Activa el usuario
        user = confirmation.user
        user.is_active = True
        
        # Si existe el campo email_confirmed, actualízalo
        if hasattr(user, 'email_confirmed'):
            user.email_confirmed = True
        
        user.save()
        
        # Marca el token como usado
        confirmation.used = True
        confirmation.save()
        
        # Respuesta HTML que incluye DOCTYPE adecuado
        html_response = """<!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Cuenta Activada - ABCPet</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    text-align: center;
                    padding: 40px 20px;
                    line-height: 1.6;
                    background-color: #f8f8f8;
                    margin: 0;
                }
                
                .success-container {
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: white;
                    border-radius: 8px;
                    padding: 30px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                
                .success-icon {
                    font-size: 60px;
                    color: #4CAF50;
                    margin-bottom: 20px;
                }
                
                h1 {
                    color: #333;
                    font-size: 24px;
                    margin-bottom: 20px;
                }
                
                .button {
                    display: inline-block;
                    background-color: #000;
                    color: white;
                    padding: 12px 30px;
                    border-radius: 4px;
                    text-decoration: none;
                    margin-top: 20px;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="success-container">
                <div class="success-icon">✓</div>
                <h1>¡Tu cuenta ha sido activada con éxito!</h1>
                <p>Gracias por verificar tu correo electrónico. Ahora puedes acceder a todos los servicios de ABCPet.</p>
                <a href="/login/" class="button">Iniciar sesión</a>
            </div>
        </body>
        </html>
        """
        response = HttpResponse(html_response)
        # Configura una política CSP más permisiva
        response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src *;"
        return response
        
    except Exception as e:
        # Manejo de error con DOCTYPE adecuado
        error_html = """<!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Error de Activación - ABCPet</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    text-align: center;
                    padding: 40px 20px;
                    line-height: 1.6;
                    background-color: #f8f8f8;
                    margin: 0;
                }
                
                .error-container {
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: white;
                    border-radius: 8px;
                    padding: 30px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                
                .error-icon {
                    font-size: 60px;
                    color: #e74c3c;
                    margin-bottom: 20px;
                }
                
                h1 {
                    color: #333;
                    font-size: 24px;
                    margin-bottom: 20px;
                }
                
                .button {
                    display: inline-block;
                    background-color: #000;
                    color: white;
                    padding: 12px 30px;
                    border-radius: 4px;
                    text-decoration: none;
                    margin-top: 20px;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-icon">⚠️</div>
                <h1>Error al procesar tu solicitud</h1>
                <p>Ocurrió un problema al intentar activar tu cuenta. Por favor, contacta a soporte técnico.</p>
                <a href="/login/" class="button">Ir al inicio de sesión</a>
            </div>
        </body>
        </html>
        """
        response = HttpResponse(error_html)
        # Configura una política CSP más permisiva
        response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src *;"
        
        
def confirm_email_simple(request, token):
    try:
        # Buscar y activar usuario por token
        confirmation = EmailConfirmationToken.objects.get(token=token)
        user = confirmation.user
        user.is_active = True
        user.save()
        
        # Generar respuesta HTML simple
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cuenta Confirmada - ABCPet</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; padding: 40px; }}
                .success {{ color: green; font-size: 24px; margin: 20px 0; }}
                .button {{ background: black; color: white; padding: 10px 20px; text-decoration: none; }}
            </style>
        </head>
        <body>
            <h1>Cuenta Confirmada</h1>
            <p class="success">¡Bienvenido {user.username}!</p>
            <p>Tu cuenta ha sido activada correctamente</p>
            <p><a href="/login/" class="button">Iniciar Sesión</a></p>
        </body>
        </html>
        """
        return HttpResponse(html)
        
    except Exception as e:
        return HttpResponse(f"Error al confirmar: {str(e)}")
    

def email_confirmed(request):
    # Lógica de la vista 'email_confirmed' aquí (puedes personalizarla según tus necesidades)
    
    # Mensaje de confirmación
    confirmation_message = "¡Tu correo electrónico ha sido confirmado correctamente!"

    # Enlace para iniciar sesión
    login_link = "email-confirmed"  # Reemplaza con la URL de tu página de inicio de sesión
    
    # Renderizar la plantilla 'email_confirmed.html' con los datos
    return render(request, 'abcpet_app/email_confirmed.html', {
        'confirmation_message': confirmation_message,
        'login_link': login_link,
    })
    
def generate_unique_username(base_username):
    while True:
        unique_username = f"{base_username}_{get_random_string(8)}"
        if not CustomUser.objects.filter(username=unique_username).exists():
            return unique_username
        

def email_confirm_invalid(request):
    # Puedes agregar cualquier lógica adicional que desees aquí
    # Por ejemplo, podrías pasar mensajes de error a la plantilla si es necesario
    error_message = "El token de confirmación de correo electrónico es inválido."

    # Renderiza la plantilla 'email_confirm_invalid.html' y pasa datos contextuales
    return render(request, 'email_confirm_invalid.html', {'error_message': error_message})

        
        
@login_required
def resend_confirmation_email(request):
    user = request.user
    if not user.is_confirmed:
        # Generar un nuevo token de confirmación
        token, created = EmailConfirmationToken.objects.get_or_create(user=user)
        if not created:
            token.token = get_random_string(64)
            token.save()

        # Construir el enlace de confirmación
        confirmation_link = request.build_absolute_uri(f'/confirm_email/{token.token}/')

        # Enviar el correo de confirmación
        send_mail(
            'Confirmación de Cuenta',
            f'Por favor, confirma tu cuenta haciendo clic en el siguiente enlace: {confirmation_link}',
            'noreply@tudominio.com',
            [user.email],
            fail_silently=False,
        )
        # Redirigir o mostrar un mensaje de éxito
        return redirect('dashboard')  # Ajusta esta redirección según tu flujo de usuario
    else:
        # El usuario ya está confirmado
        return redirect('dashboard')  # Ajusta esta redirección según tu flujo de usuario





def host_view(request):
    return render(request, 'dashboard/host.html')





def search_hosts(request):
    service = request.GET.get('service', '')  # Obtener el servicio seleccionado desde la solicitud GET
    print("Servicio seleccionado:", service)
    
    # Mapear el servicio seleccionado al campo correspondiente en el modelo ABCPetHost
    field_mapping = {
        'servicio_hotel': 'servicio_hotel',
        'servicio_en_casa_mascota': 'servicio_en_casa_mascota',
        'servicio_paseo_mascota': 'servicio_paseo_mascota',
        'servicio_guarderia': 'servicio_guarderia',
    }
    
    # Verificar si el servicio seleccionado es válido
    if service in field_mapping:
        field_name = field_mapping[service]
        # Realizar la búsqueda de cuidadores basada en el servicio en tu modelo ABCPetHost
        hosts = ABCPetHost.objects.filter(**{field_name: True})
        # Serializar los resultados si es necesario y devolverlos como JSON
        results = [{'user_id': host.user.id, 'username': host.user.username} for host in hosts]
        
        # Devolver los resultados como una respuesta JSON
        return JsonResponse({'results': results})
    else:
        return JsonResponse({'error': 'Servicio no válido'})
    
    
    
def resultados_busqueda(request):
    selected_service = request.GET.get('service', '')  # Obtén el servicio seleccionado desde la solicitud GET
    print("Servicio seleccionado:", selected_service)  # Agrega esta línea para depurar

    # Filtra los resultados según el servicio seleccionado
    if selected_service == 'servicio_hotel':
        hosts = ABCPetHost.objects.filter(servicio_hotel=True)
    elif selected_service == 'servicio_en_casa_mascota':
        hosts = ABCPetHost.objects.filter(servicio_en_casa_mascota=True)
    elif selected_service == 'servicio_paseo_mascota':
        hosts = ABCPetHost.objects.filter(servicio_paseo_mascota=True)
    elif selected_service == 'servicio_guarderia':
        hosts = ABCPetHost.objects.filter(servicio_guarderia=True)
    else:
        hosts = []  # Si el servicio no es válido, establece una lista vacía
    print("Resultados obtenidos:", hosts)  # Agrega esta línea para depurar

    # Renderiza el template con los resultados y el servicio seleccionado como contexto
    return render(request, 'abcpet_app/resultados_busqueda.html', {'resultados': hosts, 'selected_service': selected_service})



def detalle_host(request, anfitrion_id):
    
    # Obtener el objeto del anfitrión
    anfitrion = get_object_or_404(ABCPetHost, pk=anfitrion_id)
    return render(request, 'dashboard/detalle_host.html', {'anfitrion': anfitrion})


    

   
# Permite la carga simultanea de fotos en el host al crear la cuenta.
def registrar_host(request):
    if request.method == 'POST':
        form = ABCPetHostForm(request.POST, request.FILES)
        if form.is_valid():
            abcpet_host = form.save(commit=False)
            abcpet_host.user = request.user
            abcpet_host.save()
            
            # Guardar las imágenes en el álbum del anfitrión
            for image in request.FILES.getlist('album_host_images'):
                print(f"Guardando imagen: {image.name}")
                abcpet_host.album_host_images.create(image=image)

            return redirect('pagina_de_inicio')
        else:
            print(form.errors)
    else:
        form = ABCPetHostForm()
    return render(request, 'register_host.html', {'form': form})






def register_host1(request):
    if request.method == 'POST':
        if 'step' in request.POST:
            step = int(request.POST['step'])
            if step == 1:
                form = ABCPetHostForm1(request.POST, request.FILES)
                if form.is_valid():
                    host_instance = form.save(commit=False)
                    if request.user.is_authenticated:  # Verifica si el usuario está autenticado
                        host_instance.user = request.user  # Asigna el usuario autenticado
                    host_instance.save()  # Guarda la instancia en la base de datos
                    return redirect('register_host2')
                # Agrega más lógica para otros pasos del formulario aquí
        else:
            form = ABCPetHostForm1(request.POST, request.FILES)
            if form.is_valid():
                host_instance = form.save(commit=False)
                if request.user.is_authenticated:  # Verifica si el usuario está autenticado
                    host_instance.user = request.user  # Asigna el usuario autenticado
                host_instance.save()
                return redirect('dashboard') 
            # Maneja el caso si la solicitud es POST pero no se envía un paso válido
    else:
        form = ABCPetHostForm1()
    
    # Obtén el UserProfile asociado al usuario autenticado
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    
    return render(request, 'dashboard/register_host/register_host1.html', {'form': form, 'profile': profile})



def register_host2(request):
    if request.method == 'POST':
        if 'step' in request.POST:
            step = int(request.POST['step'])
            if step == 2:
                form = ABCPetHostForm2(request.POST, request.FILES)
                if form.is_valid():
                    host_instance = form.save(commit=False)
                    if request.user.is_authenticated:
                        host_instance.user = request.user
                    host_instance.save()
                    return redirect('register_host3')
                # Agrega más lógica para otros pasos del formulario aquí
        else:
            form = ABCPetHostForm2(request.POST, request.FILES)
            if form.is_valid():
                host_instance = form.save(commit=False)
                if request.user.is_authenticated:
                    host_instance.user = request.user
                host_instance.save()
                return redirect('dashboard') 
            # Maneja el caso si la solicitud es POST pero no se envía un paso válido
    else:
        form = ABCPetHostForm2()
    
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    
    return render(request, 'dashboard/register_host/register_host2.html', {'form': form, 'profile': profile})







@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante para mantener al usuario autenticado
            messages.success(request, 'Tu contraseña ha sido actualizada exitosamente.')
            return redirect('change_password')
        else:
            messages.error(request, 'Por favor, corrige los errores.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})










def admin_logout_view(request):
    logout(request)
    return redirect('/administrador/login/')






def get_client_ip(request):
    """ 
    Obtener la IP del cliente desde la solicitud.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@never_cache
def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/administrador/dashboard')
        else:
            return redirect('/usuario/dashboard')

    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        ip = get_client_ip(request)  # Obtener la IP del cliente
        try:
            user = CustomUser.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                response = redirect('/administrador/dashboard')
                response.set_cookie('saved_email', email)  # Guardar el email en una cookie
                return response
            else:
                context['error_message'] = f'Acceso no autorizado desde la IP {ip}. Abandonde el administrador.'
        except CustomUser.DoesNotExist:
            context['error_message'] = f'Acceso no autorizado desde la IP {ip}. Abandonde el administrador.'

    return render(request, 'administrador/login.html', context)

def admin_logout(request):
    logout(request)
    response = redirect('/administrador/login/')
    return response


@login_required(login_url='/administrador/login/')
def admin_dashboard(request):
    if not request.user.is_staff:
        raise PermissionDenied("No tienes permiso para acceder a esta página.")
    return render(request, 'administrador/dashboard.html')





def send_reset_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            # Marcar los códigos anteriores como usados
            PasswordResetCode.objects.filter(user=user, is_used=False).update(is_used=True)
            
            # Generar nuevo código
            code = get_random_string(6, allowed_chars='0123456789')
            PasswordResetCode.objects.create(user=user, code=code)
            
            # Preparar la plantilla HTML
            from django.template.loader import render_to_string
            from django.core.mail import EmailMultiAlternatives
            from django.urls import reverse
            import datetime
            
            # Obtener la URL base completa
            site_url = request.build_absolute_uri('/').rstrip('/')
            logo_url = f"{site_url}/static/abcpet_app/images/logo.png"
            
            # Contexto para la plantilla HTML
            context = {
                'verification_code': code,
                'user': user,
                'login_url': f"{site_url}/login/",
                'logo_url': logo_url,
                'current_year': datetime.datetime.now().year
            }
            
            # Renderizar el HTML
            html_content = render_to_string('emails/reset_password_code.html', context)
            
            # Versión de texto plano para clientes de correo que no soportan HTML
            text_content = f'Hola, solicitaste cambio de contraseña en nuestra plataforma, para continuar ingresa el siguiente codigo para actualizar tu contraseña: {code}. Considera que este codigo es válido por 15 minutos.'
            
            # Crear y enviar el correo
            subject = 'Código de restablecimiento de contraseña en abcpet.org'
            from_email = 'noreply@example.com'
            to_email = [email]
            
            email_message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            email_message.attach_alternative(html_content, "text/html")
            email_message.send(fail_silently=False)
            
            request.session['reset_email'] = email  # Guardar email en la sesión
            return redirect('verify_code')
        else:
            return render(request, 'reset_password.html', {'error': 'No existe una cuenta con ese email.'})
    return render(request, 'reset_password.html')
        
        
        

def verify_code(request):
    email = request.session.get('reset_email')
    print(f"Email retrieved from session: {email}")  # Añadir print statement para depuración
    if not email:
        return redirect('send_reset_code')  # Redirige si no hay email en la sesión
    if request.method == 'POST':
        code = request.POST.get('code')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            reset_code = PasswordResetCode.objects.filter(user=user, code=code).first()
            if reset_code and reset_code.is_valid():
                reset_code.is_used = True
                reset_code.save()
                return redirect('change_password', user_id=user.id)
            else:
                return render(request, 'verify_code.html', {'error': 'Código incorrecto o expirado', 'email': email})
    return render(request, 'verify_code.html', {'email': email})

from django.contrib.auth import update_session_auth_hash

def change_password(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Para mantener la sesión iniciada después del cambio de contraseña
        return redirect('password_changed')
    return render(request, 'change_password.html', {'user': user})


def password_changed(request):
    return render(request, 'password_changed.html')


def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session with the new password
            return redirect(reverse('login'))  # Redirect to login
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password_change_form.html', {'form': form})




def dashboard_view(request):
    # Lógica de la vista del dashboard
    return render(request, 'administrador/dashboard.html')

def user_management_view(request):
    users = CustomUser.objects.all()
    return render(request, 'administrador/user_management.html', {'users': users})

def edit_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    else:
        form = UserForm(instance=user)
    
    return render(request, 'administrador/edit_user.html', {'form': form})

def site_settings_view(request):
    # Lógica de la vista de configuración del sitio
    return render(request, 'administrador/site_settings.html')



def admin_dashboard_view(request):
    user_count = CustomUser.objects.filter(is_staff=False).count()
    staff_count = CustomUser.objects.filter(is_staff=True).count()
    return render(request, 'abcpet_app/admin_dashboard.html', {
        'user_count': user_count,
        'staff_count': staff_count
    })
    
def add_new_item(request):
    # Lógica de tu vista para agregar un nuevo elemento
    return render(request, 'abcpet_app/add_new_item.html')