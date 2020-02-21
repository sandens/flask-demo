from flask import Flask
import os
from . import db,auth,blog


def create_app(test_config=None):
    app = Flask(__name__ ,instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path,'flask.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        app.logger.info(app.instance_path)
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as e:
        raise e

    db.init_app(app)

    ## Register Blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    app.add_url_rule("/", endpoint='index')

    @app.route('/hello')
    def hello():
         return "Hello World" 

    return app       
