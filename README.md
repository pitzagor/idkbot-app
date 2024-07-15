# ExpandBot

You know this feeling, right? Every conversation, every document seems to be filled with mysterious acronyms and shortened terms. It becomes an impossible task to decipher the meaning behind a single sentence that contained those five different abbreviations. 

We have to navigate through countless Confluence pages and internal documents, juggling between them to piece together the puzzle. It is a journey of patience and persistence, and.... total wast of time :) 

**ExpandBot **is a Slack bot that comes as a result of that frustrations. It just expands abbreviations. It takes an abbreviation as input and returns its expansion. It uses simple text file in the background. You find a new abbreviation - add it to the file and update the GitHub repo! 

## The best practices 

When it comes to writing a good technical document, one of the best practices is to always expand an abbreviation the first time you use it. 

This practice ensures clarity and avoids confusion for readers who may not be familiar with the specific jargon or acronyms used in the document. By expanding the abbreviation upon its first mention, you provide context and establish a solid foundation of understanding for the readers. This approach promotes effective communication and enhances the overall readability and comprehension of the technical document.

## Installation

1. Clone the repository:
    
        bash
    
    git clone https://github.com/your-username/expandbot.git

2. Install the required dependencies:
    
        bash
    
    pip install -r requirements.txt

3. up the Slack app:

    - Create a new Slack app in your Slack workspace.
    - Enable the "Interactivity & Shortcuts" feature and set the Request URL to your server's URL (e.g., **https://your-server.com/slack/events**).
    - Enable the "Slash Commands" feature and create a new command with the following details:
        - Command: **/expandbot**
        - Request URL: **https://your-server.com/slack/events**
    - Install the app to your workspace and note down the Bot Token and Signing Secret.
4. Set up environment variables:

    - Create a **.env** file in the project root directory.
    - Add the following environment variables to the **.env** file:
        
                **SLACK_BOT_TOKEN=your-bot-token
        SLACK_SIGNING_SECRET=your-signing-secret
        PORT=3000
        **
    
    
    **    Replace `your-bot-token` and `your-signing-secret` with the respective values from your Slack app.
    
    5. Load abbreviations:
    
      - Create a file named `abbreviations.txt` in the project root directory.
      - Add abbreviations and their expansions in the following format:
        ```
        abbr1 expansion1
        abbr2 expansion2
        ...
        ```
    
    6. Run the app:
    
      ```bash
      python app.py
    **

## Usage

To use ExpandBot, you can type **/expandbot [abbreviation]** in any channel or direct message. Replace **[abbreviation]** with the abbreviation you want to expand.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://gpt.equinix.com/LICENSE).

Feel free to customize this README.md file according to your specific app and requirements.
