import os
import logging
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

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

# Initialize the Slack app and client
slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET")

app = App(token=slack_bot_token, signing_secret=slack_signing_secret)
client = WebClient(token=slack_bot_token)

# Initialize Flask app
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# Load abbreviations
abbreviations = load_abbreviations('abbreviations.txt')

# Handle the /expandobot slash command
def handle_expandobot_command(command):
    query = command['text'].strip().upper()
    if query in abbreviations:
        return f"{query}: {abbreviations[query]}"
    else:
        return f"Sorry, I couldn't find an expansion for '{query}'."

# Catch-all event handler
@app.event("*")
def handle_all_events(event, logger):
    logger.info(f"Received event: {event}")

# Error handler
@app.error
def custom_error_handler(error, body, logger):
    logger.exception(f"An error occurred: {error}")
    logger.info(f"Request body: {body}")

# Flask route for Slack events
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    logging.debug(f"Received request to /slack/events")
    logging.debug(f"Content-Type: {request.content_type}")
    logging.debug(f"Request data: {request.get_data(as_text=True)}")

    # Handle URL verification
    if request.json and request.json.get("type") == "url_verification":
        logging.info("Handling URL verification request")
        return jsonify({"challenge": request.json["challenge"]})

    # Handle slash commands (application/x-www-form-urlencoded)
    if request.form and request.form.get("command") == "/expandobot":
        logging.info("Handling /expandobot command")
        response_text = handle_expandobot_command(request.form)
        return jsonify({"response_type": "in_channel", "text": response_text})

    # Handle other events (application/json)
    logging.info("Handling other event")
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
