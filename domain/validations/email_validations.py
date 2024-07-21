import re

def validate_email(email: str) -> bool:
    pattern = r"^\S+@\S+\.\S+$"
    if re.match(pattern, email):
        return True
    else:
        raise ValueError("Correo electrónico no válido")