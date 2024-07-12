import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initialize the Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Load abbreviations from file
def load_abbreviations(file_path):
    abbreviations = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' ', 1)
            if len(parts) == 2:
                abbreviations[parts[0].upper()] = parts[1]
    return abbreviations

# Load abbreviations
abbreviations = load_abbreviations('config/abbreviations.txt')

# Handle the /expandobot slash command
@app.command("/expandobot")
def handle_expandobot_command(ack, say, command):
    ack()
    query = command['text'].strip().upper()
    if query in abbreviations:
        say(f"{query}: {abbreviations[query]}")
    else:
        say(f"Sorry, I couldn't find an expansion for '{query}'.")

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
