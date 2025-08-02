from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from .models import Rol, Usuario, PermisoPersonalizado, Red, Alerta, Dispositivos
from .serializers import (
    RolSerializer, UsuarioSerializer,
    PermisoPersonalizadoSerializer,
    RedSerializer, AlertaSerializer,
    DispositivosSerializer,
)
from .utils import (generar_token,enviar_email_recuperacion)
from .serializers import (PasswordResetSerializer)
from .permissions import (TienePermiso)


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class PermisoPersonalizadoViewSet(viewsets.ModelViewSet):
    queryset = PermisoPersonalizado.objects.all()
    serializer_class = PermisoPersonalizadoSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    """def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_usuario')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_usuario')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_usuario')()]
        return [TienePermiso('read_usuario')()]"""


class RedViewSet(viewsets.ModelViewSet):
    queryset = Red.objects.all()
    serializer_class = RedSerializer
    """def get_permissions(self):
       if self.action == 'create':
            return [TienePermiso('create_red')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_red')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_red')()]
        return [TienePermiso('read_red')()]"""

class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    """def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_alerta')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_alerta')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_alerta')()]
        return [TienePermiso('read_alerta')()]"""

class DispositivosViewSet(viewsets.ModelViewSet):
    queryset = Dispositivos.objects.all()
    serializer_class = DispositivosSerializer
    """def get_permissions(self):
        if self.action == 'create':
            return [TienePermiso('create_dispositivo')()]
        elif self.action in ['update', 'partial_update']:
            return [TienePermiso('update_dispositivo')()]
        elif self.action == 'destroy':
            return [TienePermiso('delete_dispositivo')()]
        return [TienePermiso('read_dispositivo')()]"""

class PasswordReset(APIView):  
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SolicitudRecuperacion(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({'error': 'No existe un usuario con ese email, envia un post json- "email": "usuario@correo.com"  '}, status=status.HTTP_404_NOT_FOUND)
        
        token = generar_token()
        usuario.token_recuperar = token
        usuario.save()
        
        enviar_email_recuperacion(usuario.email, token)
        return Response({'mensaje': 'Token de recuperación enviado a tu email.'}, status=status.HTTP_200_OK)

