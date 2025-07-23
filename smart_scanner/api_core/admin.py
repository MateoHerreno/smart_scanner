from django.contrib import admin
from .models import *
from django.utils.html import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(Rol)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['id','nombre','descripcion']
    ordering = ('id',)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id','cedula', 'email', 'nombre', 'password', 'rol', 'is_active')
    search_fields = ('cedula', 'nombre', )
    ordering = ('id',)

@admin.register(red)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ssid', 'password', 'url_api', 'autonomo')
    search_fields = ('nombre', )
    ordering = ('id',)

@admin.register(PermisoPersonalizado)
class PermisoPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ('accion', 'usuario', 'admin',)
    list_editable = ('usuario', 'admin',)
    search_fields = ('accion',)