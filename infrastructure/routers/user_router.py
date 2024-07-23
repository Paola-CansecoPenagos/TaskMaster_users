from flask import Blueprint
from infrastructure.controllers.register_user_controller import register_user_blueprint
from infrastructure.controllers.login_user_controller import login_user_blueprint
from infrastructure.controllers.check_user_existence_controller import check_user_existence_blueprint
from infrastructure.controllers.create_group_controller import create_group_blueprint
from infrastructure.controllers.get_group_members_controller import get_group_members_blueprint
from infrastructure.controllers.get_usernames_controller import get_usernames_blueprint
from infrastructure.controllers.add_group_members_controller import add_group_members_blueprint
from infrastructure.controllers.confirmation_controller import confirmation_blueprint

user_router = Blueprint('user_router', __name__)

user_router.register_blueprint(register_user_blueprint, url_prefix='/')
user_router.register_blueprint(login_user_blueprint, url_prefix='/')
user_router.register_blueprint(check_user_existence_blueprint, url_prefix='/')
user_router.register_blueprint(create_group_blueprint, url_prefix='/')
user_router.register_blueprint(get_group_members_blueprint, url_prefix='/')
user_router.register_blueprint(get_usernames_blueprint, url_prefix='/')
user_router.register_blueprint(add_group_members_blueprint, url_prefix='/')
user_router.register_blueprint(confirmation_blueprint, url_prefix='/confirm')