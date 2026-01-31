from flask import Blueprint, render_template, jsonify, request
from app.extensions import mongo
from datetime import datetime

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

# 1. Receiver: Captures data FROM GitHub
@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    payload = None

    if event_type == "push":
        payload = {
            "request_id": data.get('after'),
            "author": data.get('pusher', {}).get('name'),
            "action": "PUSH",
            "from_branch": None,
            "to_branch": data.get('ref', '').split('/')[-1],
            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
    elif event_type == "pull_request":
        payload = {
            "request_id": str(data.get('pull_request', {}).get('id')),
            "author": data.get('pull_request', {}).get('user', {}).get('login'),
            "action": "PULL_REQUEST",
            "from_branch": data.get('pull_request', {}).get('head', {}).get('ref'),
            "to_branch": data.get('pull_request', {}).get('base', {}).get('ref'),
            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }

    if payload:
        mongo.db.events.insert_one(payload)
        return jsonify({"status": "received"}), 200
    return jsonify({"status": "ignored"}), 200

# 2. UI Route: Shows the index.html page
@webhook.route('/')
def index():
    return render_template('index.html')

# 3. Data API: Sends MongoDB data to the UI
# 3. Data API: Sends MongoDB data to the UI
# We changed this from /display-data to /events to match your HTML fetch!
@webhook.route('/events')
def display_data():
    events = list(mongo.db.events.find().sort("timestamp", -1).limit(10))
    for e in events:
        e['_id'] = str(e['_id'])
    return jsonify(events)