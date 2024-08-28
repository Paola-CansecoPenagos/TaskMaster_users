from flask import Blueprint, jsonify
from infrastructure.repositories.user_repository import UserRepository

confirmation_blueprint = Blueprint('confirmation', __name__)

repository = UserRepository()

@confirmation_blueprint.route('/<token>', methods=['GET'])
def confirm_registration(token):
    try:
        user = repository.find_by_token(token)
        if user and not user['confirmed']:
            repository.confirm_user(user['_id'])
            return jsonify({"message": "Usuario confirmado exitosamente"}), 200
        return jsonify({"error": "Token inválido o usuario ya confirmado"}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado"}), 500
