from domain.entities.group import Group
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.repositories.group_repository import GroupRepository

class CreateGroupUseCase:
    def __init__(self, user_repository: UserRepository, group_repository: GroupRepository):
        self.user_repository = user_repository
        self.group_repository = group_repository

    def execute(self, creator_id: str, member_usernames: list):
        if len(member_usernames) > 5:
            raise ValueError("El grupo no puede tener más de 6 miembros, incluyendo al creador.")
       
        if self.group_repository.find_group_by_user_id(creator_id):
            raise ValueError("El creador ya está en un grupo.")

        members = []
        creator = self.user_repository.find_user(creator_id)
        if not creator:
            raise ValueError("El creador no existe.")

        members.append({"user_id": str(creator["_id"]), "username": creator["username"]})

        for username in member_usernames:
            user = self.user_repository.find_by_username_or_email(username, username)
            if not user:
                raise ValueError(f"El usuario {username} no existe.")
            if self.group_repository.find_group_by_user_id(str(user["_id"])):
                raise ValueError(f"El usuario {username} ya está en un grupo.")
            members.append({"user_id": str(user["_id"]), "username": user["username"]})

        group = Group(members=members)
        self.group_repository.create_group(group.dict())
