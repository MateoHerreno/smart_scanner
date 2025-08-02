# api_core/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings
from .models import Rol, PermisoPersonalizado
import json
import os

@receiver(post_migrate)
def inicializar_roles(sender, **kwargs):
    if sender.label != 'api_core':
        return

    try:
        print("[SIGNALS] Inicializando roles...")
        Rol.inicializar_roles()
    except Exception as e:
        print(f"[ERROR] No se pudieron inicializar los roles: {e}")

@receiver(post_migrate)
def inicializar_permisos(sender, **kwargs):
    if sender.label != 'api_core':
        return

    print("[SIGNALS] Inicializando permisos...")
    ruta = os.path.join(settings.BASE_DIR, 'api_core', 'zpermisos_definidos.json')
    
    if not os.path.exists(ruta):
        print(f"[ADVERTENCIA] No se encontró el archivo {ruta}")
        return

    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            permisos = json.load(f)
            for p in permisos:
                PermisoPersonalizado.objects.update_or_create(
                    accion=p["accion"],
                    defaults={
                        "admin": p.get("admin", False),
                        "usuario": p.get("usuario", False),
                    }
                )
        print("[SIGNALS] Permisos cargados correctamente.")
    except Exception as e:
        print(f"[ERROR] No se pudieron cargar los permisos: {e}")
