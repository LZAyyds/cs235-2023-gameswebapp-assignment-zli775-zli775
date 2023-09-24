from flask import Flask

from .gameDescription_bp import game_description_bp
from .home_bp import home_bp
from .games_bp import games_bp
from.search_bp import search_bp
from.login_bp import login_bp
from.user_profile_bp import user_profile_bp
from games.adapters.memory_repository import MemoryRepository, populate
import games.adapters.repository as repo
from .wishlist_bp import wishlist_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dh13828808842'
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)
    app.register_blueprint(home_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(game_description_bp)
    app.register_blueprint(wishlist_bp, url_prefix='/wishlist')
    app.register_blueprint(search_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(user_profile_bp)
    return app
def create_app(test_config=None):

    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = Path('covid') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)
    return app
