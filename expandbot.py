import os
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

expandobot = Flask(__name__)

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=SLACK_BOT_TOKEN)

def load_abbreviations():
    abbreviations = {}
    with open("abbreviations.txt", "r") as file:
        for line in file:
            abbr, expansion = line.strip().split(" ", 1)
            abbreviations[abbr.lower()] = expansion
    return abbreviations

abbreviations = load_abbreviations()

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    if "event" in data:
        event = data["event"]
        if event["type"] == "app_mention":
            handle_mention(event)

    return jsonify({"status": "ok"})

@app.route("/slack/commands", methods=["POST"])
def slack_commands():
    command = request.form.get("command")
    text = request.form.get("text", "").lower()
    channel_id = request.form.get("channel_id")

    if command == "/expandobot":
        if text in abbreviations:
            response = f"{text.upper()}: {abbreviations[text]}"
        else:
            response = f"Sorry, I don't know the expansion for '{text}'."

        try:
            client.chat_postMessage(channel=channel_id, text=response)
        except SlackApiError as e:
            print(f"Error posting message: {e}")

    return jsonify({"response_type": "in_channel"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
