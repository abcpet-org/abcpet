from django.core.mail import send_mail, EmailMultiAlternatives
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from .models import EmailConfirmationToken
from .models import OTPCode
import random
import string  
from django.utils import timezone
from datetime import timedelta
import datetime

def send_confirmation_email(user):
    token = EmailConfirmationToken.objects.create(user=user)
    confirmation_link = settings.SITE_DOMAIN + reverse('confirm_email', args=[token.token])

    subject = 'Confirma tu cuenta ABCPet'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]
    text_content = f'Please confirm your email address by clicking on this link: {confirmation_link}'
    html_content = render_to_string('emails/confirmation_email.html', {'confirmation_link': confirmation_link})

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()
    
def send_otp_email(user):
    """
    Genera un código OTP de 8 dígitos y lo envía al correo del usuario
    utilizando una plantilla HTML elegante y minimalista.
    El código expira después de 2 minutos.
    """
    # Generar código OTP aleatorio de 8 dígitos
    otp_code = ''.join(random.choices(string.digits, k=8))
    
    # Calcular tiempo de expiración (2 minutos)
    expiry_time = timezone.now() + timedelta(minutes=2)
    
    # Guardar en la base de datos
    OTPCode.objects.filter(user=user, is_used=False).update(is_used=True)  # Invalidar códigos anteriores
    OTPCode.objects.create(
        user=user,
        code=otp_code,
        expires_at=expiry_time
    )
    
    # Preparar el correo con plantilla HTML
    subject = 'Código de verificación ABCPet'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]
    
    # Contenido texto plano (alternativo para clientes que no soportan HTML)
    text_content = f"""
    Hola {user.first_name},
    
    Tu código de verificación para ABCPet es: {otp_code}
    
    Este código expirará en 2 minutos.
    
    Gracias,
    El equipo de ABCPet
    """
    
    # Preparar el contexto para la plantilla HTML
    # Nota: No podemos usar {% static %} directamente en el correo electrónico,
    # así que proporcionamos la URL completa
    logo_url = settings.SITE_DOMAIN + settings.STATIC_URL + 'abcpet_app/images/logo.png'
    
    context = {
        'user': user,
        'otp_code': otp_code,
        'login_url': settings.SITE_DOMAIN + reverse('login'),
        'current_year': datetime.datetime.now().year,
        'logo_url': logo_url
    }
    
    # Renderizar la plantilla HTML
    html_content = render_to_string('emails/otp_verification.html', context)
    
    # Crear y enviar el correo
    try:
        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()
        print(f"OTP enviado a {user.email}: {otp_code}")
    except Exception as e:
        print(f"Error al enviar OTP: {e}")
    
    return otp_code