from flask import Blueprint, request, jsonify
from datetime import datetime
from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


@webhook.route('/receiver', methods=["POST"])
def receiver():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    data = None

    # PUSH EVENT
    if event_type == "push":
        data = {
            "event_type": "push",
            "author": payload["pusher"]["name"],
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": datetime.utcnow()
        }

    # PULL REQUEST EVENT
    elif event_type == "pull_request":
        action = payload["action"]

        if action == "opened":
            data = {
                "event_type": "pull_request",
                "author": payload["pull_request"]["user"]["login"],
                "from_branch": payload["pull_request"]["head"]["ref"],
                "to_branch": payload["pull_request"]["base"]["ref"],
                "timestamp": datetime.utcnow()
            }

        elif action == "closed" and payload["pull_request"]["merged"]:
            data = {
                "event_type": "merge",
                "author": payload["pull_request"]["merged_by"]["login"],
                "from_branch": payload["pull_request"]["head"]["ref"],
                "to_branch": payload["pull_request"]["base"]["ref"],
                "timestamp": datetime.utcnow()
            }

    if data:
        mongo.db.events.insert_one(data)

    return jsonify({"status": "success"}), 200


@webhook.route('/events', methods=["GET"])
def get_events():
    events = mongo.db.events.find().sort("timestamp", -1).limit(20)

    result = []

    for e in events:
        formatted_time = e["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")

        if e["event_type"] == "push":
            text = f'{e["author"]} pushed to {e["to_branch"]} on {formatted_time}'

        elif e["event_type"] == "pull_request":
            text = f'{e["author"]} submitted a pull request from {e["from_branch"]} to {e["to_branch"]} on {formatted_time}'

        elif e["event_type"] == "merge":
            text = f'{e["author"]} merged branch {e["from_branch"]} to {e["to_branch"]} on {formatted_time}'

        result.append(text)

    return jsonify(result)
