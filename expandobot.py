import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load abbreviations from the file
abbreviations = {}
with open("abbreviations.txt", "r") as file:
    for line in file:
        abbreviation, expansion = line.strip().split(" ", 1)
        abbreviations[abbreviation.strip()] = expansion.strip()

# Initialize the Slack client
slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)

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

    @app.route("/slack/events", methods=["POST"])
    def slack_events():
        data = request.json
        if "challenge" in data:
            return data["challenge"]
        elif "event" in data and "text" in data["event"]:
            command = data["event"]["text"]
            channel = data["event"]["channel"]
            handle_command(command, channel)
        return ""

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
