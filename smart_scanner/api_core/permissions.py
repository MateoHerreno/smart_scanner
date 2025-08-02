from rest_framework.permissions import BasePermission
from .models import PermisoPersonalizado

# Mapeo de número de rol al nombre usado en la tabla
ROLES = {
    1: 'admin',
    2: 'empleado',
}

class TienePermiso:
    def __init__(self, accion):
        self.accion = accion

    def __call__(self):
        class _Permiso(BasePermission):
            def has_permission(inner_self, request, view):
                if not request.user.is_authenticated:
                    return False

                rol_nombre = ROLES.get(request.user.rol)
                if not rol_nombre:
                    return False

                try:
                    permiso = PermisoPersonalizado.objects.get(accion=self.accion)
                    return getattr(permiso, rol_nombre, False)
                except PermisoPersonalizado.DoesNotExist:
                    return False

        return _Permiso()



