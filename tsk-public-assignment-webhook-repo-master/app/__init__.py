from flask import Flask
from app.extensions import mongo
from app.webhook.routes import webhook

def create_app():
    app = Flask(__name__, template_folder='../templates')

    # This connects your app to MongoDB Atlas
    app.config["MONGO_URI"] = "mongodb+srv://karthikeyasiddu98-db-user:Siddutillu@cluster0.dsdvs3p.mongodb.net/github_events?retryWrites=true&w=majority"

    # Initialize mongo with the app
    mongo.init_app(app)
    
    app.register_blueprint(webhook)
    
    return app