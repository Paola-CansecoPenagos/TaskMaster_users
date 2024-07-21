from flask import Blueprint
from infrastructure.controllers.register_user_controller import register_user_blueprint
from infrastructure.controllers.login_user_controller import login_user_blueprint
from infrastructure.controllers.check_user_existence_controller import check_user_existence_blueprint

user_router = Blueprint('user_router', __name__)

user_router.register_blueprint(register_user_blueprint, url_prefix='/')
user_router.register_blueprint(login_user_blueprint, url_prefix='/')
user_router.register_blueprint(check_user_existence_blueprint, url_prefix='/')
