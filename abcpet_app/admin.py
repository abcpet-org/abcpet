# En tu admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from django.contrib.auth.models import User
from .models import UserProfile
from .models import UserPayment
from .models import UserWallet, Transaccion
from .models import Mascota
from django.utils.safestring import mark_safe
from .models import Mascota, MascotaFoto  # Asegúrate de tener esta línea
from django.utils.html import mark_safe
admin.site.register(MascotaFoto) 
from .models import ABCPetHost
from .models import LoginDetail
from .models import CustomUser
from .models import OTPCode



admin.site.register(LoginDetail)


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__email', 'code')

# Define una clase para personalizar la visualización del UserProfile en el admin.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'calle_numero', 'info_adicional', 'comuna', 'region', 'postal_code', 'country', 'phone_number', 'rut', 'fecha_nacimiento', 'genero', 'newsletter_email', 'newsletter_telefono')


# Registra el UserProfileAdmin con el modelo UserProfile.
admin.site.register(UserProfile, UserProfileAdmin)

# Utiliza UserAdmin para personalizar la visualización del modelo de usuario en el admin.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')


# Define una clase para personalizar la visualización del UserPayment en el admin.
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'cvc', 'expiration_date', 'card_type')
    

class TransaccionInline(admin.TabularInline):
    model = Transaccion

class UserWalletAdmin(admin.ModelAdmin):
    inlines = [TransaccionInline]
    list_display = ['user', 'balance', 'promo_used']
    readonly_fields = ['user', 'balance', 'promo_used']
    



# Desregistra el modelo User predeterminado y vuelve a registrar con CustomUserAdmin.

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserPayment)
admin.site.register(UserWallet, UserWalletAdmin)






@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'tipo_mascota',
        'nombre_mascota',
        'peso',
        'edad',
        'sexo',
        'raza',
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
    )
    
    search_fields = ['nombre_mascota', 'user__username']

    def ver_imagen(self, obj):
        return '<img src="%s" width="50" height="50" />' % obj.imagen.url if obj.imagen else ''

    ver_imagen.short_description = 'Galería de Fotos'
    
    
    
    
@admin.register(ABCPetHost)
class ABCPetHostAdmin(admin.ModelAdmin):
    list_display = ['user', 'aprobado']
    actions = ['approve_host', 'reject_host']

    def approve_host(self, request, queryset):
        queryset.update(aprobado=True)
    approve_host.short_description = "Aprobar seleccionados como anfitriones"

    def reject_host(self, request, queryset):
        queryset.update(aprobado=False)
    reject_host.short_description = "Rechazar seleccionados como anfitriones"
    
    

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('email', 'username', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser',
                       'groups', 'user_permissions')
        }),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    
admin.site.register(CustomUser, CustomUserAdmin)

