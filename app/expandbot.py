import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from flask import Flask, request

# Initialize the Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Initialize Flask app
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Your Slack bot is running!"

if __name__ == "__main__":
    # Start your Slack app
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.connect()

    # Start the Flask app
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)
