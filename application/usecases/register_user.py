from domain.entities.user import User
from domain.validations.password_validation import validate_password
from domain.validations.email_validations import validate_email
from domain.validations.username_validations import validate_username, validate_username_inappropriate
from domain.validations.text_validations import validate_text
from infrastructure.services.bcrypt_service import hash_password
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.repositories.notification_repository import NotificationRepository
from infrastructure.services.jwt_service import create_access_token
from infrastructure.services.email_service import send_confirmation_email

class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository, notification_repository: NotificationRepository):
        self.user_repository = user_repository
        self.notification_repository = notification_repository 

    def execute(self, user_data: dict):
        user = User(**user_data)
        
        validate_password(user.password)
        validate_username(user.username)
        validate_email(user.email)
        validate_username_inappropriate(user.username)

        validate_text(user.email)
        validate_text(user.password)
        validate_text(user.username)
        
        if self.user_repository.find_by_username_or_email(user.username, user.email):
            raise ValueError("El nombre de usuario o correo electrónico ya están registrados.")
        
        user.password = hash_password(user.password)
        token = create_access_token(user.email)
        send_confirmation_email(user.email, token)
        
        user_dict = user.dict()
        user_dict.update({"confirmed": False, "confirmation_token": token})
        result = self.user_repository.save_user(user_dict)
        
        notification_data = {
            "task_id": "0000000",
            "user_id": str(result.inserted_id),
            "message": "¡Bienvenido a TaskMaster! Esperamos que seas muy productivo."
        }
        self.notification_repository.create_notification(notification_data)

        return {"user_id": str(result.inserted_id)}