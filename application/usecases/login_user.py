from infrastructure.repositories.user_repository import UserRepository
from infrastructure.services.bcrypt_service import verify_password
from infrastructure.services.jwt_service import create_access_token
from domain.validations.text_validations import validate_text

class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, identifier: str, password: str):
        user = self.user_repository.find_by_username_or_email(identifier, identifier)

        if not user:
            raise ValueError("Usuario no encontrado.")

        if not verify_password(password, user['password']):
            raise ValueError("Contraseña incorrecta.")
        
        token = create_access_token(str(user['_id']))
        return {"token": token, "user_id": str(user['_id'])}
