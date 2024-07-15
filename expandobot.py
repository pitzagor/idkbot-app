import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request

# Load abbreviations from a file
def load_abbreviations(file_path):
    abbreviations = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(' ', 1)
            abbreviations[key.lower()] = value
    return abbreviations

# Initialize the Slack app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Load the abbreviations
abbreviations = load_abbreviations('abbreviations.txt')

# Command handler for /expandbot
@app.command("/expandbot")
def handle_expandobot(ack, respond, command):
    ack()
    abbreviation = command['text'].strip().lower()

    if not abbreviation:
        respond("Please provide an abbreviation as an argument."
        return

    expansion = abbreviations.get(abbreviation)

    if not expansion:
        respond(f"No expansion found for abbreviation: {abbreviation.upper()}")
    
    respond(f"{abbreviation.upper()}: {expansion}")

# Flask web server for Slack events
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# Start your app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    flask_app.run(host='0.0.0.0', port=port)
