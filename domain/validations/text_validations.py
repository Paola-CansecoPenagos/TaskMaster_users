import re

def validate_text(text):
    patterns = [
        r"<script.*?>.*?</script>",
        r"<iframe.*?>.*?</iframe>",
        r"<(object|embed|applet|link|style|img|meta|base).*?>",
        r"on[a-z]+=\"[^\"]*\"",
        r"href=\"javascript:[^\"]*\"",
        r"src=\"javascript:[^\"]*\"",
        r"style=\".*?expression\([^)]*\).*?\""
    ]
    if any(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in patterns):
        raise ValueError("El email, username o contraseña contiene contenido no permitido.")
