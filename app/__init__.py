from flask import Flask
from app.webhook.routes import webhook
from app.extensions import init_mongo


def create_app():

    app = Flask(__name__)

    # Initialize MongoDB
    init_mongo(app)

    # Register blueprint
    app.register_blueprint(webhook)

    return app
