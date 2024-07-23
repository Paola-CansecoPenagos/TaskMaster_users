from infrastructure.repositories.group_repository import GroupRepository

class GetGroupMembersUseCase:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    def execute(self, user_id: str):
        group = self.group_repository.find_group_by_user_id(user_id)
        if not group:
            raise ValueError("El usuario no pertenece a ningún grupo.")
        
        members = [{"user_id": member['user_id'], "username": member['username']} for member in group['members']]
        return members