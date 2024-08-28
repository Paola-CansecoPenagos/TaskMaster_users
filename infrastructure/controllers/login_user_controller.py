from flask import Blueprint, request, jsonify
from application.usecases.login_user import LoginUserUseCase
from infrastructure.repositories.user_repository import UserRepository
from utils.text_utils import escape_html, escape_javascript

login_user_blueprint = Blueprint('login_user', __name__)

repository = UserRepository()
login_user_usecase = LoginUserUseCase(user_repository=repository)

@login_user_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    try:
        result = login_user_usecase.execute(data['identifier'], data['password'])
        return jsonify({"access_token": result["token"], "user_id": result["user_id"]}), 200
    except ValueError as e:
        print(f"Error de validación: {str(e)}") 
        return jsonify({"error": "Credenciales inválidas"}), 400
    except Exception as e:
        print(f"Error inesperado: {str(e)}") 
        return jsonify({"error": "Ocurrió un error inesperado"}), 500
