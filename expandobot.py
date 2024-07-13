import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Load abbreviations from a file
def load_abbreviations(file_path):
    abbreviations = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(' ', 1)
            abbreviations[key.lower()] = value
    return abbreviations

# Initialize the Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Load the abbreviations
abbreviations = load_abbreviations('abbreviations.txt')

# Command handler for /expandobot
@app.command("/expandobot")
def handle_expandobot(ack, respond, command):
    ack()
    abbreviation = command['text'].strip().lower()
    expansion = abbreviations.get(abbreviation, "Abbreviation not found")
    respond(f"{abbreviation.upper()}: {expansion}")

# Start your app
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
