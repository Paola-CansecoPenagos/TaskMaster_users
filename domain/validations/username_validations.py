import re

def validate_username(username: str) -> bool:
    if not 3 <= len(username) <= 20:
        raise ValueError("El nombre de usuario debe tener entre 3 y 20 caracteres.")
    return True
