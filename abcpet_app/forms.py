import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

from .models import UserPayment
from .models import Mascota
from multiupload.fields import MultiFileField
from .models import MascotaFoto
from django import forms
from django.utils.translation import gettext as _
from .models import ABCPetHost
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from abcpet_app.models import CustomUser
from .models import CustomUser
from django.core.exceptions import ValidationError
from .models import HostImage
from .models import ABCPetHost
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from .models import CustomUser





User = get_user_model()

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

    def clean_username(self):
        email = self.cleaned_data['username']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No existe un usuario con este correo electrónico.")
        return email
    








# Definición de la función para determinar el tipo de tarjeta
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



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)  # Cambia a False
    first_name = forms.CharField(max_length=150, required=False, label="Nombre")  # Cambia a False

    class Meta:
        model = CustomUser
        fields = ("first_name", "username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        initial_email = kwargs.pop('initial_email', None)
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # Establecer el valor inicial del campo de correo electrónico
        if initial_email:
            self.fields['email'].initial = initial_email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False  # Establecer 'username' como no requerido
    
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if not any(char.isupper() for char in password1):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        return password1
    
    
class CustomUserStep4Form(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre de usuario'}))
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su apellido'}))
    







class HiddenCardNumberInput(forms.widgets.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            value = '*' * (len(value) - 4) + value[-4:]
        return super().render(name, value, attrs, renderer)

class UserPaymentForm(forms.ModelForm):
    class Meta:
        model = UserPayment
        fields = ['card_number', 'cvc', 'expiration_date']
        widgets = {
            'card_number': HiddenCardNumberInput(),
        }

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']

        # Verifica si el número de tarjeta es válido y determina el tipo
        card_type = self.determine_card_type(card_number)

        if card_type == 'Desconocido':
            raise forms.ValidationError('No pudimos determinar el tipo de su tarjeta. Por favor, verifique y vuelva a intentar.')

        if card_type not in ['Visa', 'Mastercard']:
            raise forms.ValidationError('Solo se aceptan tarjetas Visa o Mastercard.')

        return card_number

    def determine_card_type(self, card_number):
        # Utiliza un patrón para determinar el tipo de tarjeta
        visa_pattern = re.compile(r'^4[0-9]{12}(?:[0-9]{3})?$')
        mastercard_pattern = re.compile(r'^5[1-5][0-9]{14}$')

        if visa_pattern.match(card_number):
            return 'Visa'
        elif mastercard_pattern.match(card_number):
            return 'Mastercard'
        else:
            return 'Desconocido'
        
        
        
        
class PromoCodeForm(forms.Form):
    promo_code = forms.CharField(max_length=50)
    
#override de cambios para form edit_profile. (insertado)




class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['data_sharing_enabled', 'service_related_settings']
        labels = {
            'data_sharing_enabled': 'Habilitar Compartir Datos',
            'service_related_settings': 'Configuración de Servicios Relacionados',
        }
        widgets = {
            'service_related_settings': forms.Textarea(attrs={'rows': 4}),
        }
        
        
        
from django import forms
from .models import Mascota
from multiupload.fields import MultiFileField

class MascotaForm(forms.ModelForm):
    galeria_fotos = MultiFileField(min_num=1, max_num=6, max_file_size=1024 * 1024 * 5)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['consume_medicacion'].widget.attrs.update({'class': 'consume-medicacion-checkbox', 'style': 'transform: scale(1.5);'})

    class Meta:
        model = Mascota
        fields = [
            'nombre_mascota',
            'tipo_mascota',
            'raza',
            'peso',
            'edad',
            'sexo',
            'con_microchip',
            'esterilizado_castrado',
            'amigable_con_ninos',
            'amigable_con_perros',
            'fecha_adopcion_nacimiento',
            'sobre_tu_mascota',
            'nivel_energia',
            'horario_alimentacion',
            'puede_dejar_solo',
            'medicamentos',
            'detalles_medicacion',
            'algo_mas_ninera_deba_saber',
            'informacion_veterinaria',
            'proveedor_seguro_mascotas',
            'consume_medicacion',
        ]

        widgets = {
            'fecha_adopcion_nacimiento': forms.DateInput(attrs={'type': 'date', 'placeholder': 'DD-MM-YYYY'}),
            'raza': forms.Select(attrs={'data-tipo-mascota-url': '/obtener_razas/'}),
            'informacion_veterinaria': forms.TextInput(attrs={'placeholder': 'Ingrese los datos de su veterinaria'}),
            'proveedor_seguro_mascotas': forms.TextInput(attrs={'placeholder': 'Si su mascota tiene un seguro, ingrese el nombre de la compañía'}),
            'sobre_tu_mascota': forms.Textarea(attrs={'style': 'height: 100px; width: 100%;', 'placeholder': 'Escribe una breve descripción sobre tu mascota, ayudara en tus reservaciones con Super Amigos.'}),
            'algo_mas_ninera_deba_saber': forms.Textarea(attrs={'style': 'height: 100px; width: 100%;', 'placeholder': 'Por favor, proporciona cualquier información adicional que la sitter debería saber, como la alimentación, las rutinas, las alergias, etc.'}),
            'detalles_medicacion': forms.Textarea(attrs={'style': 'height: 100px; width: 100%;'}),      
        }  
        
  

    def save(self, commit=True):
        mascota = super(MascotaForm, self).save(commit=False)

        # Resto del código...

        # Crea instancias de MascotaFoto para cada archivo cargado
        for uploaded_file in self.files.getlist('file'):
            MascotaFoto.objects.create(mascota=mascota, imagen=uploaded_file)

        if commit:
            mascota.save()

        return mascota
    
    
    
    
    
    class MascotaNombreForm(forms.Form):
        nombre_mascota = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
        
    
    
class MultipleFileInput(forms.ClearableFileInput):
    template_name = 'django/forms/widgets/clearable_file_input.html'

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['multiple'] = True

    def format_value(self, value):
        """
        Return an HTML snippet for rendering.
        """
        if not value:
            return ''
        return mark_safe(self.template_with_initial.format(
            initial=self.initial_text,
            input=self.html_input_text,
            clear_template=self.clear_template,
            value=', '.join(str(item) for item in value),
        ))
    
    


class ABCPetHostForm(forms.ModelForm):
    DIAS_SEMANA_OPCIONES = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    TIPOS_MASCOTAS_OPCIONES = [
        ('Perro pequeño (0-7 Kg)', 'Perro pequeño (0-7 Kg)'),
        ('Perro mediano (7-15 Kg)', 'Perro mediano (7-15 Kg)'),
        ('Perro grande (15-45 Kg)', 'Perro grande (15-45 Kg)'),
        ('Perro gigante (más de 46 Kg)', 'Perro gigante (más de 46 Kg)'),
        ('Gato', 'Gato'),
    ]

    TIPO_VIVIENDA_OPCIONES = [
        ('Casa', 'Casa'),
        ('Departamento', 'Departamento'),
        ('Parcela o sitio', 'Parcela o sitio'),
    ]

    TIPO_JARDIN_OPCIONES = [
        ('Patio cercado', 'Patio cercado'),
        ('Patio sin cerca', 'Patio sin cerca'),
        ('Sin patio', 'Sin patio'),
    ]

    POLITICA_CANCELACION_OPCIONES = [
        ('Mismo día', 'Mismo día'),
        ('Un día', 'Un día'),
        ('Tres días', 'Tres días'),
        ('Siete días', 'Siete días'),
    ]

    dias_disponibles = forms.MultipleChoiceField(
        choices=DIAS_SEMANA_OPCIONES,
        widget=forms.CheckboxSelectMultiple
    )
    tipos_mascotas = forms.MultipleChoiceField(
        choices=TIPOS_MASCOTAS_OPCIONES,
        widget=forms.CheckboxSelectMultiple
    )
    tipo_vivienda = forms.ChoiceField(choices=TIPO_VIVIENDA_OPCIONES)
    tipo_jardin = forms.ChoiceField(choices=TIPO_JARDIN_OPCIONES)
    politica_cancelacion = forms.ChoiceField(choices=POLITICA_CANCELACION_OPCIONES)

    # Utilizamos MultipleFileInput para permitir la carga de múltiples archivos
    album_host_images = forms.ImageField(widget=MultipleFileInput(), required=False)
    

    class Meta:
        model = ABCPetHost
        fields = '__all__'
        exclude = ['user', 'aprobado']
        widgets = {
            'expectativas_casa': forms.Textarea(attrs={'rows': 4}),
            'experiencia_cuidado_mascotas': forms.Textarea(attrs={'rows': 4}),
            'rutina_diaria': forms.Textarea(attrs={'rows': 4}),
            # Puedes agregar más widgets según sea necesario
        }


class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        # Agrega aquí todos los campos de CustomUser que desees editar
        
        
        
class EditProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ['calle_numero', 'info_adicional', 'comuna', 'region', 'postal_code', 'country', 'profile_picture', 'phone_number', 'rut', 'fecha_nacimiento', 'genero', 'newsletter_email', 'newsletter_telefono']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'last_name': forms.HiddenInput(),
            
            # Otros widgets según sea necesario
        }
        
    
        
        
        
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        # Establecer valores iniciales para campos que son None
        if self.instance:
            if self.instance.country is None or self.instance.country.strip() == '':
                self.initial['country'] = 'Chile'





class ABCPetHostForm1(forms.ModelForm):
    TIPOS_CUENTA = [
        ('Hotel', 'Hotel'),
        ('En casa de la mascota', 'En casa de la mascota'),
        ('Paseo mascota', 'Paseo mascota'),
        ('Guarderia', 'Guarderia'),
        # Añadir más tipos de cuenta según sea necesario
    ]

    tipo_cuenta = forms.ChoiceField(choices=TIPOS_CUENTA, label='Tipo de Cuenta', required=False)

    class Meta:
        model = ABCPetHost
        fields = '__all__'
        


class ABCPetHostForm2(forms.ModelForm):
    TIPOS_CUENTA = [
        ('Hotel', 'Hotel'),
        ('En casa de la mascota', 'En casa de la mascota'),
        ('Paseo mascota', 'Paseo mascota'),
        ('Guarderia', 'Guarderia'),
        # Añadir más tipos de cuenta según sea necesario
    ]

    tipo_cuenta = forms.ChoiceField(choices=TIPOS_CUENTA, label='Tipo de Cuenta', required=False)

    class Meta:
        model = ABCPetHost
        fields = '__all__'
        
        

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Contraseña antigua",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label="Confirma nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    
    
    
class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']  # Ajusta los campos según tus necesidades