# Facebook Auto Comment Bot

This is a simple Flask-based Facebook Auto Comment Bot that schedules and posts comments automatically.

## Deployment on Render

1. Clone this repo or upload it to GitHub.
2. Create a new **Web Service** on [Render](https://render.com/).
3. Use the following build & start commands:
   ```sh
   pip install -r requirements.txt
   python app.py
   ```
4. Open the Render-provided URL to use the bot.

## Features

- Takes **Access Token, Post Link, Time** from the user.
- Saves details in `data.txt`.
- Uses **Facebook Graph API** to post a comment.
- Runs automatically at the scheduled time.
