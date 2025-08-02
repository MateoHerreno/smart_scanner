from django.urls import path, include
#from django.contrib.auth.models import User
#from rest_framework import routers, serializers, viewsets
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RolViewSet, UsuarioViewSet,
    PermisoPersonalizadoViewSet,
    RedViewSet, AlertaViewSet,
    DispositivosViewSet,SolicitudRecuperacion, PasswordReset,
)

router = DefaultRouter()
router.register(r'roles', RolViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'permisos', PermisoPersonalizadoViewSet)
router.register(r'redes', RedViewSet)
router.register(r'alertas', AlertaViewSet)
router.register(r'dispositivos', DispositivosViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/passrequest/', SolicitudRecuperacion.as_view(), name='passrequest'), 
    path('api/passreset/', PasswordReset.as_view(), name='passreset'),
]
