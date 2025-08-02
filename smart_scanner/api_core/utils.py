from django.core.mail import send_mail
from django.conf import settings
import secrets

def generar_token():
    token = secrets.token_urlsafe(6)  # token ~8 caracteres
    token = token[:8]  # asegúrate de que tenga exactamente 8 
    return f"{token[:4]}-{token[4:]}" #parte el token con un guion

def enviar_email_recuperacion(email, token):
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    
    asunto = "Recuperación de contraseña"
    mensaje = (
        f"Hola,\n\n"
        f"Has solicitado cambiar tu contraseña.\n"
        f"Tu token de recuperación es:\n\n"
        f"{token}\n\n"
        f"Utiliza este token para cambiar tu contraseña en la aplicación.\n\n"
        f"Tambien puedes ir a la url... \n\n"
        f"restablecer?email={email}&token={token}\n\n"
        f"¡Gracias!"
    )
    from_email = None  # usa el DEFAULT_FROM_EMAIL en "contable/contabilidad/contabilidad/setings.py"
    recipient_list = [email]
    send_mail(asunto, mensaje, from_email, recipient_list)