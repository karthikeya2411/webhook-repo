from flask_pymongo import PyMongo

mongo = PyMongo()

def init_mongo(app):
    app.config["MONGO_URI"] = "mongodb+srv://preethihja_db_user:fgvtYxdflQ8MmRty@cluster0.flmdnv4.mongodb.net/github_events?retryWrites=true&w=majority"
    mongo.init_app(app)
