import os
import requests
from flask import Flask, request, jsonify
from github import Github

app = Flask(__name__)

# Initialize GitHub client
g = Github(os.environ.get('GITHUB_TOKEN'))

# Replace with your repository details
REPO_OWNER = 'your-github-username'
REPO_NAME = 'your-repo-name'
FILE_PATH = 'abbreviations.txt'

def get_abbreviations():
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    file_content = repo.get_contents(FILE_PATH).decoded_content.decode('utf-8')
    return dict(line.strip().split(' ', 1) for line in file_content.splitlines())

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    if data['type'] == 'url_verification':
        return jsonify({'challenge': data['challenge']})
    return '', 200

@app.route('/slack/commands', methods=['POST'])
def slack_command():
    command_text = request.form['text'].upper()
    abbreviations = get_abbreviations()
    
    if command_text in abbreviations:
        response = f"{command_text}: {abbreviations[command_text]}"
    else:
        response = f"Sorry, I couldn't find an expansion for '{command_text}'."
    
    return jsonify({
        'response_type': 'in_channel',
        'text': response
    })

if __name__ == '__main__':
    app.run(port=3000)
