import re

def validate_password(password: str) -> bool:
    if len(password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    if not re.search("[a-z]", password):
        raise ValueError("La contraseña debe incluir al menos una letra minúscula.")
    if not re.search("[A-Z]", password):
        raise ValueError("La contraseña debe incluir al menos una letra mayúscula.")
    if not re.search("[0-9]", password):
        raise ValueError("La contraseña debe incluir al menos un número.")
    if not re.search("[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};:'\",<>\./\?]", password):
        raise ValueError("La contraseña debe incluir al menos un carácter especial.")
    return True
