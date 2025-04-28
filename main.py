import os
import requests
import time
from flask import Flask, request, render_template_string, session
from threading import Thread

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Global variables
comments = []
post_id = None
speed = None
target_name = None
token = None
stop_flags = {}  # New dictionary to control stopping

# Developer details
user_name = "😈 𝙈𝙀 𝘿𝙀𝙑𝙄𝙇 ᯽ 𝙊𝙉 𝙁𝙄𝙍𝙀 😈"
whatsapp_no = "9024870456"

# Function to read comments from uploaded file
def read_comments_from_file(uploaded_file):
    global comments
    comments = uploaded_file.read().decode("utf-8").splitlines()
    comments = [comment.strip() for comment in comments if comment.strip()]

# Function to post comments
def post_comment(user_id):
    comment_index = 0
    while True:
        if stop_flags.get(user_id, False):
            print(f"User {user_id} stopped commenting.")
            break
        
        if not comments:
            print("No comments to post!")
            break

        comment = comments[comment_index % len(comments)]
        url = f"https://graph.facebook.com/{post_id}/comments"
        params = {
            "message": comment,
            "access_token": token
        }
        response = requests.post(url, params=params)

        if response.status_code == 200:
            print(f"[{user_id}] Comment posted: {comment}")
        else:
            print(f"[{user_id}] Failed to post comment: {response.text}")

        comment_index += 1
        time.sleep(speed)

# Function to start background commenting
def start_commenting(user_id):
    thread = Thread(target=post_comment, args=(user_id,))
    thread.daemon = True
    thread.start()

@app.route("/", methods=["GET", "POST"])
def index():
    global post_id, speed, target_name, token

    if request.method == "POST":
        user_id = session.get('user_id')
        if not user_id:
            user_id = str(time.time())
            session['user_id'] = user_id

        action = request.form.get('action')

        if action == "stop":
            stop_flags[user_id] = True
            return f"User {user_id} has requested to stop commenting."

        post_id = request.form["post_id"]
        speed = int(request.form["speed"])
        target_name = request.form["target_name"]
        token = request.form["single_token"]

        # Handle uploaded comments file
        if 'comments_file' in request.files:
            uploaded_file = request.files['comments_file']
            if uploaded_file.filename:
                read_comments_from_file(uploaded_file)

        stop_flags[user_id] = False  # Reset stop flag
        start_commenting(user_id)

        return f"User {user_id} started posting comments!"

    return render_template_string(f"""
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Auto Comment Bot</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f0f0f0; text-align: center; }}
                form {{ background: white; padding: 20px; margin: auto; width: 300px; margin-top: 50px; border-radius: 10px; box-shadow: 0px 0px 10px grey; }}
                input, button {{ width: 100%; padding: 10px; margin: 10px 0; }}
                button {{ background: green; color: white; border: none; cursor: pointer; }}
                .stop-btn {{ background: red; }}
                .header {{ font-size: 24px; font-weight: bold; }}
                .footer {{ margin-top: 20px; font-size: 16px; color: gray; }}
            </style>
        </head>
        <body>
            <h2>Facebook Auto Comment Bot</h2>
            <p class="header">Welcome to the Facebook Auto Comment Bot!</p>
            <p>Developer: {user_name}</p>
            <p>For any help, contact via WhatsApp: {whatsapp_no}</p>
            <form action="/" method="post" enctype="multipart/form-data">
                <input type="text" name="post_id" placeholder="Enter Post ID" required>
                <input type="text" name="speed" placeholder="Enter Speed (seconds)" required>
                <input type="text" name="target_name" placeholder="Enter Target Name" required>
                
                <label>Single Token:</
