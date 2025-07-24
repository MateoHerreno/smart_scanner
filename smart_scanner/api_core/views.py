from django.shortcuts import render
from rest_framework import viewsets
from .models import Rol, Usuario, PermisoPersonalizado, Red, Alerta, Dispositivos
from .serializers import (
    RolSerializer, UsuarioSerializer,
    PermisoPersonalizadoSerializer,
    RedSerializer, AlertaSerializer,
    DispositivosSerializer,
)

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class PermisoPersonalizadoViewSet(viewsets.ModelViewSet):
    queryset = PermisoPersonalizado.objects.all()
    serializer_class = PermisoPersonalizadoSerializer

class RedViewSet(viewsets.ModelViewSet):
    queryset = Red.objects.all()
    serializer_class = RedSerializer

class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer

class DispositivosViewSet(viewsets.ModelViewSet):
    queryset = Dispositivos.objects.all()
    serializer_class = DispositivosSerializer
