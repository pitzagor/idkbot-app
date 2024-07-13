import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request, jsonify
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load abbreviations from file
def load_abbreviations(file_path):
    abbreviations = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(' ', 1)
                if len(parts) == 2:
                    abbreviations[parts[0].upper()] = parts[1]
    except FileNotFoundError:
        logging.warning(f"Warning: Abbreviations file not found at {file_path}")
    return abbreviations

# Initialize the Slack app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Initialize Flask app
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# Load abbreviations
abbreviations = load_abbreviations('abbreviations.txt')

# Handle the /expandobot slash command
@app.command("/expandobot")
def handle_expandobot_command(ack, say, command):
    ack()
    query = command['text'].strip().upper()
    if query in abbreviations:
        say(f"{query}: {abbreviations[query]}")
    else:
        say(f"Sorry, I couldn't find an expansion for '{query}'.")

# Flask route for Slack events
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    logging.debug(f"Received event: {request.json}")
    # Check if this is a URL verification request
    if request.json and request.json.get("type") == "url_verification":
        # Respond with the challenge token
        return jsonify({"challenge": request.json["challenge"]})
    return handler.handle(request)    

# Home route
@flask_app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "Expandobot is running!"})

# Error handling
@flask_app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Not found"}), 404

@flask_app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == "__main__":
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    
    # Start the Flask app
    flask_app.run(host="0.0.0.0", port=port)
