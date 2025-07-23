from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, cedula, nombre, email, password=None, **extra_fields):
        if not cedula:
            raise ValueError("El campo 'cedula' es obligatorio.")
        if not email:
            raise ValueError("El campo 'email' es obligatorio.")
        if not nombre:
            raise ValueError("El campo 'nombre' es obligatorio.")

        email = self.normalize_email(email)
        user = self.model(cedula=cedula, nombre=nombre, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, nombre, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not password:
            raise ValueError(_('El superusuario debe tener una contraseña.'))

        return self.create_user(cedula=cedula, nombre=nombre, email=email, password=password, **extra_fields)
