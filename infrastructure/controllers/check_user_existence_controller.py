from flask import Blueprint, request, jsonify
from application.usecases.check_user_existence import CheckUserExistenceUseCase
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.services.jwt_service import decode_access_token  

check_user_existence_blueprint = Blueprint('check_user_existence', __name__)

repository = UserRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterU')
check_user_existence_usecase = CheckUserExistenceUseCase(user_repository=repository)

@check_user_existence_blueprint.route('/user-exists', methods=['GET'])
def check_user_exists():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "No authorization token provided"}), 401

    token = auth_header.split(' ')[1]
    user_info = decode_access_token(token)
    if not user_info:
        return jsonify({"error": "Invalid or expired token"}), 401

    user_id = user_info.get('user_id')
    if not isinstance(user_id, str):
        return jsonify({f"error": "Invalid user_id format"}), 400
    
    if check_user_existence_usecase.execute(user_id):
        return jsonify({f"exists": True}), 200
    else: 
        return jsonify({f"exists": False}), 404
    