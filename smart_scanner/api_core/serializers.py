from rest_framework import serializers
from .models import Rol, Usuario, PermisoPersonalizado, Red, Alerta, Dispositivos

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre', 'cedula',
            'password', 'password2', 'is_active',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop('password', None)
        rep.pop('password2', None)
        return rep

    def validate(self, data):
        password = data.get('password')
        password2 = self.initial_data.get('password2')

        if self.instance is None:
            if not password or not password2:
                raise serializers.ValidationError({
                    'password2': 'Debes confirmar la contraseña.'
                })
            if password != password2:
                raise serializers.ValidationError({
                    'password2': 'Las contraseñas no coinciden.'
                })
        else:
            if password:
                if not password2:
                    raise serializers.ValidationError({
                        'password2': 'Debes confirmar la nueva contraseña.'
                    })
                if password != password2:
                    raise serializers.ValidationError({
                        'password2': 'Las contraseñas no coinciden.'
                    })

        return data

    def validate_cedula(self, value):
        usuario_actual = self.instance
        if Usuario.objects.exclude(pk=usuario_actual.pk if usuario_actual else None).filter(cedula=value).exists():
            raise serializers.ValidationError("Esta cédula ya está registrada por otro usuario.")
        return value


    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            usuario._modificado_por = request.user

        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            instance._modificado_por = request.user

        instance.save()
        return instance

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

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token_recuperar = serializers.CharField()
    nueva_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirmar_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        if data['nueva_password'] != data['confirmar_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def save(self):
        email = self.validated_data['email']
        token = self.validated_data['token_recuperar']
        nueva_password = self.validated_data['nueva_password']

        try:
            usuario = Usuario.objects.get(email=email, token_recuperar=token)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Email o token de recuperación inválido.")

        usuario.set_password(nueva_password)
        usuario.token_recuperar = "sin cambios pendientes"  # Limpia el token
        usuario.save()
        return usuario