from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django import forms
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.contrib.auth.models import User
import uuid
from multiselectfield import MultiSelectField
from .constants import DIAS_SEMANA
from django.apps import AppConfig

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .host_image import HostImage
from multiselectfield import MultiSelectField
from django.utils import timezone
from datetime import timedelta


















class UserProfile(models.Model):
    REGIONES_CHILE = [
        ('Región Metropolitana', 'Región Metropolitana'),
        ('Otra', 'Otra'),
    ]
    
    COMUNAS_SANTIAGO = [
        ('Alhué', 'Alhué'),
    ('Buin', 'Buin'),
    ('Calera de Tango', 'Calera de Tango'),
    ('Cerrillos', 'Cerrillos'),
    ('Cerro Navia', 'Cerro Navia'),
    ('Colina', 'Colina'),
    ('Conchalí', 'Conchalí'),
    ('Curacaví', 'Curacaví'),
    ('El Bosque', 'El Bosque'),
    ('El Monte', 'El Monte'),
    ('Estación Central', 'Estación Central'),
    ('Huechuraba', 'Huechuraba'),
    ('Independencia', 'Independencia'),
    ('Isla de Maipo', 'Isla de Maipo'),
    ('La Cisterna', 'La Cisterna'),
    ('La Florida', 'La Florida'),
    ('La Granja', 'La Granja'),
    ('La Pintana', 'La Pintana'),
    ('La Reina', 'La Reina'),
    ('Lampa', 'Lampa'),
    ('Las Condes', 'Las Condes'),
    ('Lo Barnechea', 'Lo Barnechea'),
    ('Lo Espejo', 'Lo Espejo'),
    ('Lo Prado', 'Lo Prado'),
    ('Macul', 'Macul'),
    ('Maipú', 'Maipú'),
    ('María Pinto', 'María Pinto'),
    ('Melipilla', 'Melipilla'),
    ('Ñuñoa', 'Ñuñoa'),
    ('Padre Hurtado', 'Padre Hurtado'),
    ('Paine', 'Paine'),
    ('Pedro Aguirre Cerda', 'Pedro Aguirre Cerda'),
    ('Peñaflor', 'Peñaflor'),
    ('Peñalolén', 'Peñalolén'),
    ('Pirque', 'Pirque'),
    ('Providencia', 'Providencia'),
    ('Pudahuel', 'Pudahuel'),
    ('Puente Alto', 'Puente Alto'),
    ('Quilicura', 'Quilicura'),
    ('Quinta Normal', 'Quinta Normal'),
    ('Recoleta', 'Recoleta'),
    ('Renca', 'Renca'),
    ('San Bernardo', 'San Bernardo'),
    ('San Joaquín', 'San Joaquín'),
    ('San José de Maipo', 'San José de Maipo'),
    ('San Miguel', 'San Miguel'),
    ('San Pedro', 'San Pedro'),
    ('San Ramón', 'San Ramón'),
    ('Santiago', 'Santiago'),
    ('Talagante', 'Talagante'),
    ('Tiltil', 'Tiltil'),
    ('Vitacura', 'Vitacura')
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    calle_numero = models.CharField(max_length=255, blank=True, null=True, verbose_name="Calle y Número")
    info_adicional = models.CharField(max_length=255, blank=True, null=True, verbose_name="Información Adicional")
    comuna = models.CharField(max_length=255, choices=COMUNAS_SANTIAGO, default='Valor por Defecto', verbose_name="Comuna")
    region = models.CharField(max_length=100, choices=REGIONES_CHILE, default='Valor por Defecto', verbose_name="Región")
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    data_sharing_enabled = models.BooleanField(default=False)
    service_related_settings = models.CharField(max_length=255, blank=True, null=True)
    rut = models.CharField(max_length=12, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=20, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro'), ('Prefiero no decirlo', 'Prefiero no decirlo')], blank=True)
    newsletter_email = models.BooleanField(default=False)
    newsletter_telefono = models.BooleanField(default=False)
    desea_verificacion = models.BooleanField(default=False, blank=True)


    
    

    
    def __str__(self):
        return self.user.username
    


#modelo de datos para generar codigo de 8 digitos, confirmación de cuenta ABCPET..
class OTPCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    

class UserPayment(models.Model):
    user = models.ForeignKey('abcpet_app.CustomUser', on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    cvc = models.CharField(max_length=3)
    expiration_date = models.CharField(max_length=5, help_text='Formato DD/AA')
    card_type = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.card_number}'







class UserWallet(models.Model):
    user = models.ForeignKey('abcpet_app.CustomUser', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    promo_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

class Transaccion(models.Model):
    wallet = models.ForeignKey(UserWallet, related_name='transacciones', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        UserWallet.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_wallet(sender, instance, **kwargs):
    instance.userwallet.save()








class LoginDetail(models.Model):
    user = models.ForeignKey('abcpet_app.CustomUser', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.ip_address} - {self.timestamp}"
    
    
    
class LoginDetail(models.Model):
    user = models.ForeignKey('abcpet_app.CustomUser', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.ip_address} - {self.timestamp}"

    @classmethod
    def get_login_details(cls, user):
        return cls.objects.filter(user=user).order_by('-timestamp')
    
    
    



class Mascota(models.Model):
    user = models.ForeignKey('abcpet_app.CustomUser', on_delete=models.CASCADE)

    # Detalles de la mascota
    TIPO_CHOICES = [("Perro", _("Perro")), ("Gato", _("Gato"))]
    tipo_mascota = models.CharField(max_length=10, choices=TIPO_CHOICES)
    raza = models.CharField(max_length=255)
    nombre_mascota = models.CharField(max_length=255)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    edad = models.IntegerField()
    SEXO_CHOICES = [("Macho", _("Macho")), ("Hembra", _("Hembra"))]
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    

    # Detalles adicionales
    con_microchip = models.BooleanField(default=False)
    esterilizado_castrado = models.BooleanField(default=False)
    amigable_con_ninos = models.BooleanField(default=False)
    amigable_con_perros = models.BooleanField(default=False)
    fecha_adopcion_nacimiento = models.DateField()
    sobre_tu_mascota = models.TextField()

    # Información de cuidado
    ENERGIA_CHOICES = [("Alto", _("Alto")), ("Medio", _("Medio")), ("Bajo", _("Bajo"))]
    nivel_energia = models.CharField(max_length=10, choices=ENERGIA_CHOICES)
    HORARIO_ALIMENTACION_CHOICES = [("Manana", _("Mañana")), ("Tarde", _("Tarde")), ("Noche", _("Noche"))]
    horario_alimentacion = models.CharField(max_length=20, choices=HORARIO_ALIMENTACION_CHOICES)
    DEJAR_SOLO_CHOICES = [("1_2_horas", _("1 a 2 horas")), ("2_4_horas", _("2 a 4 horas")), ("4_12_horas", _("4 a 12 horas")), ("12_24_horas", _("12 a 24 horas"))]
    puede_dejar_solo = models.CharField(max_length=20, choices=DEJAR_SOLO_CHOICES)
    
    
    consume_medicacion = models.BooleanField(default=False)
    
    
    
    medicamentos = models.CharField(max_length=255, blank=True, null=False)
    detalles_medicacion = models.TextField(blank=True, null=True)
    algo_mas_ninera_deba_saber = models.TextField()



    # Información de salud
    informacion_veterinaria = models.TextField()
    proveedor_seguro_mascotas = models.CharField(max_length=255, blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.consume_medicacion:
            self.detalles_medicacion = ""  # Limpia el campo si no consume medicación
        super().save(*args, **kwargs)
    
    
    @staticmethod
    def get_razas_por_tipo(tipo_mascota):
        razas_perro = ['Seleciona la raza de tu Perro', 'Mestizo','Afghan Hound','Airedale Terrier', 'Akita Americano', 'Akita Inu', 'Alaskan Malamute', 'American Staffordshire Terrier', 'Australian Cattle Dog', 'Australian Shepherd', 'Basenji', 'Basset Hound', 'Beagle', 'Beagle Harrier', 'Bedlington Terrier', 'Bernese Mountain Dog', 'Bichón Frisé', 'Bichón Habanero', 'Bichón Maltés', 'Bobtail', 'Bóxer', 'Boyero', 'Boyero de Australia', 'Boyero de Berna', 'Boyero de Flandes', 'Braco Alemán de pelo corto', 'Braco Alemán de pelo duro', 'Braco de Weimar', 'Briard', 'Brittany Spaniel', 'Bull Terrier', 'Bulldog', 'Bulldog Americano', 'Bulldog Campeiro', 'Bulldog Francés', 'Bulldog Inglés', 'Cairn Terrier', 'Cane Corso', 'Caniche Enano', 'Caniche Gigante', 'Caniche Toy', 'Cavalier King Charles Spaniel', 'Chesapeake Bay Retriever', 'Chihuahua', 'Chihuahua de pelo corto', 'Chihuahua de pelo largo', 'Chin Japonés', 'Chow Chow', 'Cirneco del Etna', 'Clumber Spaniel', 'Cobrador Dorado', 'Cobrador Negro', 'Cocker Spaniel', 'Collie', 'Coonhound', 'Corgi Galés de Cardigan', 'Corgi Galés de Pembroke', 'Cotón de Tulear', 'Curly-Coated Retriever', 'Dachshund', 'Dachshund de pelo corto', 'Dachshund de pelo largo', 'Dálmata', 'Dandie Dinmont Terrier', 'Doberman Pinscher', 'Dogo', 'Dogo Argentino', 'Dogo Canario', 'Dogo de Burdeos', 'Elkhound Noruego', 'Eskimo Americano', 'Eskimo Miniatura', 'Field Spaniel', 'Fila Brasileiro', 'Flat-Coated Retriever', 'Fox Terrier', 'Fox Terrier de Pelo Duro', 'Fox Terrier de Pelo Liso', 'Galgo', 'Galgo Español', 'Galgo Italiano', 'Golden Retriever', 'Gran Danés', 'Gran Pirineo', 'Gran Sabueso Anglofrancés Tricolor', 'Gran Sabueso Azul de Gascuña', 'Gran Sabueso Suizo', 'Greyhound', 'Grifón de Bruselas', 'Grifón de Pelo Duro', 'Harrier', 'Havanese', 'Husky Siberiano', 'Irish Red and White Setter', 'Irish Setter', 'Irish Terrier', 'Irish Wolfhound', 'Jack Russell Terrier', 'Japanese Chin', 'Japanese Spitz', 'Kai Ken', 'Keeshond', 'Kerry Blue Terrier', 'King Charles Spaniel', 'Klee Kai', 'Komondor', 'Kuvasz', 'Labrador Retriever', 'Lagotto Romagnolo', 'Lakeland Terrier', 'Leonberger', 'Lhasa Apso', 'Löwchen', 'Malinois', 'Maltese', 'Manchester Terrier', 'Mastiff', 'Mastín Napolitano', 'Miniature Schnauzer', 'Mudi', 'Norfolk Terrier', 'Norwegian Buhund', 'Norwich Terrier', 'Nova Scotia Duck Tolling Retriever', 'Otterhound', 'Ovejero Croata', 'Ovejero de Shiloh', 'Papillon', 'Parson Russell Terrier', 'Pastor Alemán', 'Pastor Australiano', 'Pastor Belga Laekenois', 'Pastor Belga Malinois', 'Pastor Belga Tervueren', 'Pastor de Anatolia', 'Pastor de Brie', 'Pastor de Shetland', 'Pastor Polaco de Tierras Bajas', 'Pekingese', 'Pembroke Welsh Corgi', 'Perdiguero de Burgos', 'Perdiguero Portugués', 'Perro Crestado Chino', 'Perro de Agua Español', 'Perro de Canaan', 'Perro de Montaña Bernés', 'Perro de Pastor Mallorquín', 'Perro de Presa Canario', 'Perro de Presa Mallorquín', 'Perro Esquimal Americano', 'Perro Esquimal Canadiense', 'Perro Lobo Checoslovaco', 'Perro sin Pelo del Perú', 'Petit Basset Griffon Vendeen', 'Pharaoh Hound', 'Pinscher Miniatura', 'Pit Bull Terrier', 'Podenco Canario', 'Podenco Ibicenco', 'Podenco Portugués', 'Pointer Alemán', 'Pomerania', 'Poodle', 'Poodle Miniatura', 'Poodle Toy', 'Pug', 'Retriever de Nueva Escocia', 'Rottweiler', 'Samoyedo', 'Schnauzer Gigante', 'Schnauzer Miniatura', 'Scottish Terrier', 'Setter Gordon', 'Setter Irlandés', 'Shar Pei', 'Shetland Sheepdog', 'Shiba Inu', 'Shih Tzu', 'Siberian Husky', 'Staffordshire Bull Terrier', 'Terranova', 'Terrier Chileno', 'Terrier Ruso Negro', 'West Highland White Terrier', 'Whippet', 'Yorkshire Terrier']
        razas_gato = ['Seleciona la raza de tu Gato', 'Doméstico Común', 'Persa', 'Siamés', 'Maine Coon', 'Bengalí', 'Sphynx', 'Ragdoll', 'Manx', 'British Shorthair', 'Scottish Fold', 'Otro raza Gato']
        if tipo_mascota == 'Perro':
            return razas_perro
        elif tipo_mascota == 'Gato':
            return razas_gato
        else:
            return []
        
        

 

    
    
    
class MascotaFoto(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='mascota_photos/', default='mascota_photos/default.jpg')
    fecha_subida = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Foto de {self.mascota.nombre_mascota}'
    
    
    
    
    
    
    



class MultipleChoiceField(models.TextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar el campo MultipleChoiceField manualmente
        self.fields['dias_disponibles_paseo'] = forms.MultipleChoiceField(
            choices=ABCPetHost.DIAS_SEMANA,
            required=False,  # Establecerlo como requerido o no según tus necesidades
            widget=forms.CheckboxSelectMultiple,
        )
        # Agregar el campo horarios_disponibles_paseo manualmente
        self.fields['horarios_disponibles_paseo'] = forms.MultipleChoiceField(
            choices=ABCPetHost.HORARIOS,
            required=False,  # Establecerlo como requerido o no según tus necesidades
            widget=forms.CheckboxSelectMultiple,
        )

    def from_db_value(self, value, expression, connection):
        if value is None:
            return []
        return value.split(',')

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return []
        return value.split(',')

    def get_prep_value(self, value):
        if value is None:
            return ''
        return ','.join(value)

    def formfield(self, **kwargs):
        kwargs['choices'] = self.choices
        return super().formfield(**kwargs)
    
    


class ABCPetHost(models.Model):
    # Relación con el modelo de usuario
    user = models.OneToOneField('abcpet_app.CustomUser', on_delete=models.CASCADE, unique=True, blank=True)

    

    # Servicios y sus tarifas
    servicio_hotel = models.BooleanField(default=True, verbose_name="Hotel",blank=True)
    tarifa_hotel = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(35000)], verbose_name="Tarifa Hotel")

    servicio_en_casa_mascota = models.BooleanField(default=True, verbose_name="En casa de la mascota",blank=True)
    tarifa_cuidado_casa = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(35000)], verbose_name="Tarifa Cuidado en Casa")

    servicio_paseo_mascota = models.BooleanField(default=True, verbose_name="Paseo mascota",blank=True)
    tarifa_paseo_perros = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(35000)], verbose_name="Tarifa Paseo Perros")

    servicio_guarderia = models.BooleanField(default=True, verbose_name="Guardería",blank=True)
    tarifa_guarderia = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(35000)], verbose_name="Tarifa Guardería")

    DIAS_SEMANA = (
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    )

    dias_disponibles_paseo = models.CharField(max_length=100, choices=DIAS_SEMANA, blank=True, verbose_name="Días disponibles para paseo")
    HORARIOS = (
        ('6_11', '6 - 11 AM'),
        ('11_15', '11 AM - 15 PM'),
        ('15_22', '15 PM - 22 PM'),
        ('ninguno', 'Ninguno'),
    )

    horarios_disponibles_paseo = models.CharField(max_length=100, choices=HORARIOS, blank=True, verbose_name="Horarios disponibles para paseo")
    radio_servicio_paseo = models.PositiveIntegerField(blank=True, null=True, verbose_name="Radio de servicio en KM")
    maximo_clientes_por_dia = models.PositiveIntegerField(blank=True, null=True, verbose_name="Máximo de clientes por día")

    # Datos de localización y preferencias
    COMUNAS_SANTIAGO = (
        ('las_condes', 'Las Condes'),
        ('vitacura', 'Vitacura'),
        # Añadir más opciones según sea necesario
    )

    comuna_host = models.CharField(max_length=255, choices=COMUNAS_SANTIAGO, default='las_condes', verbose_name="Comuna para Host", blank=True)
    direccion = models.CharField(max_length=200, default='Valor por Defecto', blank=True)
    region = models.CharField(max_length=100, default='Metropolitana', choices=(('Metropolitana', 'Metropolitana'),), blank=True)

    # Disponibilidad y preferencias
    en_casa_tiempo_completo = models.BooleanField(blank=True, null=True,)
    dias_disponibles = models.CharField(max_length=100, blank=True) 
    aviso_previo = models.CharField(max_length=100, blank=True)

    tipo_vivienda = models.CharField(max_length=100, blank=True)
    tipo_jardin = models.CharField(max_length=100, blank=True)
    expectativas_casa = models.TextField(blank=True)

    # Preferencias adicionales
    mascotas_varias_familias = models.BooleanField(blank=True, null=True)
    cachorros_menos_1_ano = models.BooleanField(blank=True, null=True)
    perros_sin_entrenar = models.BooleanField(blank=True, null=True)
    machos_no_castrados = models.BooleanField(blank=True, null=True)
    hembras_no_esterilizadas = models.BooleanField(blank=True, null=True)
    hembras_en_celo = models.BooleanField(blank=True, null=True)
    perros_juguetones = models.BooleanField(blank=True, null=True)
    gatos_sin_esterilizar_castrar = models.BooleanField(blank=True, null=True)

    # Políticas y referencias
    politica_cancelacion = models.CharField(max_length=100, blank=True)
    email_referencia1 = models.EmailField(blank=True)
    email_referencia2 = models.EmailField(blank=True)

    # Experiencia y descripción personal
    anos_experiencia = models.IntegerField(blank=True, null=True)
    titular_atractivo = models.CharField(max_length=200, blank=True)
    experiencia_cuidado_mascotas = models.TextField(blank=True)
    rutina_diaria = models.TextField(blank=True)

    # Fotos y verificación
    foto_perfil = models.ImageField(upload_to='fotos_perfil', blank=True, null=True)
    foto_identificacion = models.ImageField(upload_to='fotos_id', blank=True, null=True)
    comprobante_domicilio = models.ImageField(upload_to='fotos_domicilio', blank=True, null=True)
    fotos_casa = models.ImageField(upload_to='fotos_casa', blank=True, null=True)

    # Verificación de cuenta y aprobación
    desea_verificacion = models.BooleanField(blank=True, null=True)
    aprobado = models.BooleanField(default=False, blank=True)

    # Nuevo campo para el álbum de imágenes del host
    album_host_images = models.ImageField(upload_to='album_host_images', blank=True, null=True)

    
    


    ESTADO_VERIFICACION = (
        ('si', 'Verificado'),
        ('no', 'No Verificado'),
        ('pendiente', 'Pendiente de Verificación'),
    )

    estado_verificacion = models.CharField(max_length=20, choices=ESTADO_VERIFICACION, default='pendiente', verbose_name="Estado de Verificación", blank=True)

    def __str__(self):
        return self.user.username if self.user else 'Anfitrión sin Usuario'

    def is_config_complete(self):
        # Verifica si los campos obligatorios están llenos
        campos_obligatorios = [
            self.aprobado,  # Asumiendo que es obligatorio
        ]

        return all(campos_obligatorios)

    

class DiaDisponible(models.Model):
    dia = models.CharField(max_length=100, choices=ABCPetHost.DIAS_SEMANA, verbose_name="Día disponible para paseo", blank=True)
    def __str__(self):
        return self.dia

 
    
    



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_confirmed = models.BooleanField(default=False)  # Nuevo campo para confirmación de email

    def __str__(self):
        return self.username
    
    


class EmailConfirmationToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    

    

    
    

class PasswordResetCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        now = timezone.now()
        expiration_time = self.created_at + timedelta(minutes=15)
        return now <= expiration_time and not self.is_used