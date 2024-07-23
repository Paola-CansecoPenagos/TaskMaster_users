import re
from .word_validations import inappropriate_dictionary

def validate_username(username: str) -> bool:
    if not 3 <= len(username) <= 20:
        raise ValueError("El nombre de usuario debe tener entre 3 y 20 caracteres.")
    return True

def validate_username_inappropriate(username: str) -> bool:
    tokens = re.findall(r'\w+', username.lower())
    for token in tokens:
        if token in inappropriate_dictionary:
            raise ValueError("El nombre de usuario contiene palabras inapropiadas.")
    return True