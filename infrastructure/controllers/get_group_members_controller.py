from flask import Blueprint, request, jsonify
from application.usecases.get_group_members import GetGroupMembersUseCase
from infrastructure.repositories.group_repository import GroupRepository
from infrastructure.services.jwt_service import decode_access_token

get_group_members_blueprint = Blueprint('get_group_members', __name__)

group_repository = GroupRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterU')
get_group_members_usecase = GetGroupMembersUseCase(group_repository=group_repository)

@get_group_members_blueprint.route('/group-members', methods=['GET'])
def get_group_members():
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

    try:
        members = get_group_members_usecase.execute(user_id)
        return jsonify({"members": members}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado"}), 500
