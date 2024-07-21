from domain.entities.user import User
from domain.validations.password_validation import validate_password
from domain.validations.email_validations import validate_email
from domain.validations.username_validations import validate_username
from domain.validations.text_validations import validate_text
from infrastructure.services.bcrypt_service import hash_password
from infrastructure.repositories.user_repository import UserRepository

class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_data: dict):
        user = User(**user_data)
        
        validate_password(user.password)
        validate_username(user.username)
        validate_email(user.email)

        validate_text(user.email)
        validate_text(user.password)
        validate_text(user.username)
        
        if self.user_repository.find_by_username_or_email(user.username, user.email):
            raise ValueError("El nombre de usuario o correo electrónico ya están registrados.")
        
        user.password = hash_password(user.password)
        
        self.user_repository.save_user(user.dict())
