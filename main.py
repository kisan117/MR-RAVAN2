import os
import requests
import schedule
import time
import random
from flask import Flask, request, render_template_string
import threading

app = Flask(__name__)

# Constants
TOKENS_FILE = "tokens.txt"
COOKIES_FILE = "cookies.txt"
COMMENTS_FILE = "comments.txt"  # File to store comments

# Global variable for stop flag
stop_flag = False

# Load tokens from file (or default single token if file is empty)
def load_tokens():
    if os.path.exists(TOKENS_FILE) and os.path.getsize(TOKENS_FILE) > 0:
        with open(TOKENS_FILE, "r", encoding="utf-8") as file:
            tokens = [line.strip() for line in file.readlines()]
    else:
        tokens = [input("Enter Access Token: ").strip()]
    return tokens

# Load cookies (if needed)
def load_cookies():
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, "r", encoding="utf-8") as file:
            cookies = {line.split('=')[0].strip(): line.split('=')[1].strip() for line in file.readlines()}
    else:
        cookies = {}
    return cookies

# Load comments from file
def load_comments():
    if os.path.exists(COMMENTS_FILE) and os.path.getsize(COMMENTS_FILE) > 0:
        with open(COMMENTS_FILE, "r", encoding="utf-8") as file:
            comments = [line.strip() for line in file.readlines()]
    else:
        comments = ["This is an auto-generated comment!"]  # Default comment
    return comments

# Function to post comment
def post_comment():
    global stop_flag
    tokens = load_tokens()  # Load multiple or single tokens
    cookies = load_cookies()  # Load cookies if available
    comments = load_comments()  # Load comments from file
    
    # Get target name, post ID, and speed from global variables or user input
    post_id = data.get("POST_ID")
    target_name = data.get("TARGET_NAME")
    speed = float(data.get("SPEED", 1))  # Speed in seconds

    # Handle missing post ID or token
    if not post_id or not tokens:
        print("❌ Error: Missing Post ID or Token")
        return

    selected_token = random.choice(tokens)  # Randomly select a token from the list

    # Randomly select a comment from the list of loaded comments
    comment_text = random.choice(comments).replace("{TARGET_NAME}", target_name)

    url = f"https://graph.facebook.com/{post_id}/comments"
    params = {"message": comment_text, "access_token": selected_token}

    # Sending the request with cookies and token
    response = requests.post(url, params=params, cookies=cookies)

    if response.status_code == 200:
        print(f"✅ Comment posted successfully for target: {target_name}")
    else:
        print(f"❌ Failed to post comment: {response.text}")
    
    # Delay between comments as per the speed value
    time.sleep(speed)

    if stop_flag:  # Stop if stop flag is set
        return

# Function to save the user input and schedule the task
def save_and_schedule():
    post_id = input("Enter Post ID: ")
    speed = input("Enter Comment Speed (in seconds): ")
    target_name = input("Enter Target Name (Comma-separated, optional): ")

    if not post_id or not speed:
        print("❌ Error: Missing required fields.")
        return

    global data
    data = {
        "POST_ID": post_id,
        "SPEED": speed,
        "TARGET_NAME": target_name
    }

    schedule.every().day.at("00:00").do(post_comment)  # Schedule it to run daily at midnight
    print("✅ Data saved & comment scheduled successfully!")

# Route for form and to handle POST request
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        token = request.form.get("token")
        post_id = request.form.get("post_id")
        speed = request.form.get("speed")
        target_name = request.form.get("target_name", "")

        if not token or not post_id or not speed:
            return "❌ Error: Missing required fields."

        # Saving input data to global data variable
        global data
        data = {
            "POST_ID": post_id,
            "SPEED": speed,
            "TARGET_NAME": target_name
        }

        # Start comment posting in a new thread
        global stop_flag
        stop_flag = False  # Ensure the stop flag is reset
        threading.Thread(target=post_comment).start()  # Run the posting in a separate thread

        return "✅ Data saved & comment scheduled successfully!"

    return render_template_string(open("templates/index.html").read())

# Route for stopping the comments
@app.route("/stop", methods=["POST"])
def stop():
    global stop_flag
    stop_flag = True  # Set stop flag to True to stop comments
    return "✅ Comments stopped successfully!"

if __name__ == "__main__":
    save_and_schedule()  # Initial call to save & schedule
    app.run(host="0.0.0.0", port=5000, debug=True)
