from flask import Blueprint, request, jsonify
from application.usecases.get_all_usernames_except import GetAllUsernamesExceptUseCase
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.services.jwt_service import decode_access_token  

get_usernames_blueprint = Blueprint('get_usernames', __name__)

repository = UserRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterU')
get_usernames_usecase = GetAllUsernamesExceptUseCase(user_repository=repository)

@get_usernames_blueprint.route('/usernames', methods=['GET'])
def get_usernames():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "No authorization token provided"}), 401

    token = auth_header.split(' ')[1]
    user_info = decode_access_token(token)
    if not user_info:
        return jsonify({"error": "Invalid or expired token"}), 401

    user_id = user_info.get('user_id')
    if not isinstance(user_id, str):
        return jsonify({"error": "Invalid user_id format"}), 400

    usernames = get_usernames_usecase.execute(user_id)
    return jsonify(usernames), 200
