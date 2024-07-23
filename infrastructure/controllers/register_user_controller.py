from flask import Blueprint, request, jsonify
from application.usecases.register_user import RegisterUserUseCase
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.repositories.notification_repository import NotificationRepository

register_user_blueprint = Blueprint('register_user', __name__)

repository = UserRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterU')
notification_repository = NotificationRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterNot')
register_user_usecase = RegisterUserUseCase(user_repository=repository, notification_repository=notification_repository)

@register_user_blueprint.route('/', methods=['POST'])
def register_user():
    data = request.get_json()
    try:
        register_user_usecase.execute(data)
        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except ValueError as e:
        print(f"Error de validación: {str(e)}") 
        return jsonify({"error": "El registro falló debido a una entrada inválida"}), 400
    except Exception as e:
        print(f"Error inesperado: {str(e)}") 
        return jsonify({"error": "Ocurrió un error inesperado"}), 500
