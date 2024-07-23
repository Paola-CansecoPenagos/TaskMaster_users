from flask import Blueprint, request, jsonify
from application.usecases.create_group import CreateGroupUseCase
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.repositories.group_repository import GroupRepository
from infrastructure.services.jwt_service import decode_access_token

create_group_blueprint = Blueprint('create_group', __name__)

user_repository = UserRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterU')
group_repository = GroupRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterU')
create_group_usecase = CreateGroupUseCase(user_repository=user_repository, group_repository=group_repository)

@create_group_blueprint.route('/create-group', methods=['POST'])
def create_group():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "No authorization token provided"}), 401

    token = auth_header.split(' ')[1]
    user_info = decode_access_token(token)
    if not user_info:
        return jsonify({"error": "Invalid or expired token"}), 401

    creator_id = user_info.get('user_id')
    if not creator_id:
        return jsonify({"error": "Invalid user_id"}), 400

    data = request.get_json()
    member_usernames = data.get('member_usernames', [])

    try:
        create_group_usecase.execute(creator_id, member_usernames)
        return jsonify({"message": "Grupo creado exitosamente"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado"}), 500
