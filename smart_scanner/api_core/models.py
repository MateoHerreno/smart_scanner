from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from .authentication import CustomUserManager

class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=254)

    def __str__(self):
        return self.nombre

    @staticmethod
    def inicializar_roles():
        roles = ["administrador", "operador"] 
        for nombre in roles:
            Rol.objects.get_or_create(nombre=nombre)

class Usuario(AbstractBaseUser, PermissionsMixin):
    cedula = models.IntegerField(unique=True, validators=[MinValueValidator(0)])
    nombre = models.CharField(max_length=254)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254)
    token_recuperar = models.CharField(max_length=254, blank=True, default="sin cambios pendientes")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    rol = models.ForeignKey('api_core.Rol', on_delete=models.PROTECT, null=True, default=2)

    USERNAME_FIELD = "cedula"
    REQUIRED_FIELDS = ["nombre", "email"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.cedula} - {self.nombre}"

    def save(self, *args, **kwargs):
        # Validación de rol (opcional)
        usuario_modificando = getattr(self, '_modificado_por', None)
        if usuario_modificando and isinstance(usuario_modificando, Usuario):
            """if self.rol < usuario_modificando.rol:
                raise ValidationError("No puedes asignar un rol superior al tuyo.")"""
        super().save(*args, **kwargs)

class PermisoPersonalizado(models.Model):
    accion = models.CharField(max_length=100, unique=True)
    admin = models.BooleanField(default=False)
    usuario = models.BooleanField(default=False)  
    def __str__(self):
        return self.accion
    
class Red(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    ssid = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, unique=True)
    url_api = models.CharField(max_length=100, unique=True)
    autonomo = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Alerta(models.Model):
    usuario = models.ForeignKey('api_core.Usuario', on_delete=models.CASCADE,)
    ubicacion = models.CharField(max_length=265)
    fecha_hora = models.DateTimeField()
    estado = models.BooleanField(default=False)

    def __str__(self):
        return f"Alerta de {self.usuario} en {self.ubicacion} el {self.fecha_hora}"

class Dispositivos(models.Model):
    mac = models.CharField(max_length=265)
    usuario = models.ForeignKey('api_core.Usuario', on_delete=models.CASCADE,)
    mensaje = models.CharField(max_length=265)
    fecha_hora = models.DateTimeField()
    configuracion= models.CharField(max_length=265)

    def __str__(self):
        return f"{self.usuario}"
