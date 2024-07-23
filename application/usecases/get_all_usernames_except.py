from infrastructure.repositories.user_repository import UserRepository

class GetAllUsernamesExceptUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str):
        return self.user_repository.get_all_usernames_except(user_id)
