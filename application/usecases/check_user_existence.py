from infrastructure.repositories.user_repository import UserRepository

class CheckUserExistenceUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str) -> bool:
        user = self.user_repository.find_user(user_id)
        return user is not None
