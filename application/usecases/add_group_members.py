from infrastructure.repositories.user_repository import UserRepository
from infrastructure.repositories.group_repository import GroupRepository

class AddGroupMembersUseCase:
    def __init__(self, user_repository: UserRepository, group_repository: GroupRepository):
        self.user_repository = user_repository
        self.group_repository = group_repository

    def execute(self, user_id: str, new_member_usernames: list):
        group = self.group_repository.find_group_by_user_id(user_id)
        if not group:
            raise ValueError("El usuario no pertenece a ningún grupo.")

        current_member_count = len(group['members'])
        if current_member_count + len(new_member_usernames) > 6:
            raise ValueError("El grupo no puede tener más de 6 miembros.")

        new_members = []
        for username in new_member_usernames:
            user = self.user_repository.find_by_username_or_email(username, username)
            if not user:
                raise ValueError(f"El usuario {username} no existe.")
            if self.group_repository.find_group_by_user_id(str(user["_id"])):
                raise ValueError(f"El usuario {username} ya está en un grupo.")
            new_members.append({"user_id": str(user["_id"]), "username": user["username"]})

        self.group_repository.add_members_to_group(str(group['_id']), new_members)
