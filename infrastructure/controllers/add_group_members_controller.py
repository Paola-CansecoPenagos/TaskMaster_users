from flask import Blueprint, request, jsonify
from application.usecases.add_group_members import AddGroupMembersUseCase
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.repositories.group_repository import GroupRepository
from infrastructure.services.jwt_service import decode_access_token

add_group_members_blueprint = Blueprint('add_group_members', __name__)

user_repository = UserRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterU')
group_repository = GroupRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterU')
add_group_members_usecase = AddGroupMembersUseCase(user_repository=user_repository, group_repository=group_repository)

@add_group_members_blueprint.route('/add-group-members', methods=['POST'])
def add_group_members():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "No authorization token provided"}), 401

    token = auth_header.split(' ')[1]
    user_info = decode_access_token(token)
    if not user_info:
        return jsonify({"error": "Invalid or expired token"}), 401

    user_id = user_info.get('user_id')
    if not user_id:
        return jsonify({"error": "Invalid user_id"}), 400

    data = request.get_json()
    new_member_usernames = data.get('new_member_usernames', [])

    try:
        add_group_members_usecase.execute(user_id, new_member_usernames)
        return jsonify({"message": "Miembros agregados exitosamente"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado"}), 500
