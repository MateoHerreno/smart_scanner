from rest_framework import serializers
from .models import Rol, Usuario, PermisoPersonalizado, Red, Alerta, Dispositivos

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Excluye password en lectura:
        exclude = ('password',)

class PermisoPersonalizadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermisoPersonalizado
        fields = '__all__'

class RedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Red
        fields = '__all__'

class AlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields = '__all__'

class DispositivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivos
        fields = '__all__'
