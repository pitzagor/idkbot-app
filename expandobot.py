import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request, jsonify

# Load abbreviations from the file
abbreviations = {}
with open("abbreviations.txt", "r") as file:
    for line in file:
        abbreviation, expansion = line.strip().split(" ", 1)
        abbreviations[abbreviation.strip()] = expansion.strip()

# Initialize the Slack client
slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)

# Initialize the Flask app
app = Flask(__name__)

# Handle the slash command
def handle_command(command, channel):
    abbreviation = command.strip()
    if abbreviation in abbreviations:
        expansion = abbreviations[abbreviation]
        response = f"{abbreviation}: {expansion}"
    else:
        response = f"Sorry, I don't know the expansion for '{abbreviation}'."

    try:
        client.chat_postMessage(channel=channel, text=response)
    except SlackApiError as e:
        print(f"Error posting message to Slack: {e.response['error']}")

# Start the bot
if __name__ == "__main__":
    from flask import Flask, request

    app = Flask(__name__)

@app.route('/slack/events', methods=['POST'])
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
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "Expandobot is running!"})

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == "__main__":
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))

    # Start the Flask app
    app.run(host="0.0.0.0", port=port)
