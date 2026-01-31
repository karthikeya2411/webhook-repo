from flask import Flask
from app.extensions import mongo
from app.webhook.routes import webhook

def create_app():
    app = Flask(__name__)

    # Replace the URI below with your actual MongoDB connection string from Step 1
    app.config["MONGO_URI"] = "mongodb+srv://karthikeyasiddu98-db-user:Siddutillu@cluster0.dsdvs3p.mongodb.net/github_events?retryWrites=true&w=majority"

    # Initialize MongoDB with the app
    mongo.init_app(app)
    
    # Register blueprints
    app.register_blueprint(webhook)
    
    return app