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
stop_flags = {}

# Developer details
user_name = "😈 𝙈𝙀 𝘿𝙀𝙑𝙄𝙇 ᯽ 𝙊𝙉 𝙁𝙄𝙍𝙀 😈"
whatsapp_no = "9024870456"

def read_comments_from_file(uploaded_file):
    global comments
    comments = uploaded_file.read().decode("utf-8").splitlines()
    comments = [comment.strip() for comment in comments if comment.strip()]

def read_token_from_file():
    global token
    try:
        # Check for any token file (like rishi.txt or tokens.txt)
        token_files = ['tokens.txt', 'rishi.txt', 'token_file.txt']  # Add more file names if needed
        for token_file in token_files:
            if os.path.exists(token_file):
                with open(token_file, 'r') as file:
                    token = file.readline().strip()
                    print(f"Using token from file: {token}")
                    break  # Exit once we find a valid token
        if not token:
            print("No token found in the listed files.")
    except Exception as e:
        print(f"Error while reading token from file: {str(e)}")

def post_comment(user_id):
    comment_index = 0
    while True:
        if stop_flags.get(user_id, False):
            print(f"User {user_id} stopped commenting.")
            break
        
        if not comments:
            print("No comments found.")
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
            print(f"[{user_id}] Failed: {response.text}")

        comment_index += 1
        time.sleep(speed)

def start_commenting(user_id):
    thread = Thread(target=post_comment, args=(user_id,))
    thread.daemon = True
    thread.start()

@app.route("/", methods=["GET", "POST"])
def index():
    global post_id, speed, target_name

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

        # Use the token from the form if provided, else use the token from the file
        global token
        token_from_form = request.form.get('single_token')
        if token_from_form:
            token = token_from_form
            print(f"Using token from form: {token}")
        else:
            # If no token from form, use the one from the file
            if not token:
                read_token_from_file()

        if 'comments_file' in request.files:
            uploaded_file = request.files['comments_file']
            if uploaded_file.filename:
                read_comments_from_file(uploaded_file)

        stop_flags[user_id] = False
        start_commenting(user_id)

        return f"User {user_id} started posting comments!"

    # Read token from the file when the app starts (if no token is already set)
    if not token:
        read_token_from_file()

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MR DEVIL POST SERVER</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f0f0;
            text-align: center;
            margin: 0;
            padding: 0;
        }

        form {
            background: white;
            padding: 15px;
            margin: 30px auto;
            width: 90%;
            max-width: 400px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px grey;
            box-sizing: border-box;
        }

        input, button {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            font-size: 16px;
            box-sizing: border-box;
        }

        button {
            background: green;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }

        .stop-btn {
            background: red;
        }

        .header {
            font-size: 24px;
            font-weight: bold;
        }

        .footer {
            margin-top: 20px;
            font-size: 14px;
            color: gray;
        }

        /* Mobile-specific adjustments */
        @media (max-width: 600px) {
            .header {
                font-size: 20px;
            }

            form {
                padding: 10px;
            }

            input, button {
                padding: 10px;
                font-size: 14px;
            }

            .footer {
                font-size: 12px;
            }
        }
    </style>
</head>
<body>
    <h2>MR DEVIL POST SERVER</h2>
    <p class="header">Welcome to the MR DEVIL POST SERVER!</p>
    <p>Developer: {{ user_name }}</p>
    <p>For any help, contact via WhatsApp: {{ whatsapp_no }}</p>
    <form action="/" method="post" enctype="multipart/form-data">
        <input type="text" name="post_id" placeholder="Enter Post ID" required>
        <input type="text" name="speed" placeholder="Enter Speed (seconds)" required>
        <input type="text" name="target_name" placeholder="Enter Target Name" required>

        <label>Single Token (Optional):</label>
        <input type="text" name="single_token" placeholder="Enter Token (Optional)">

        <label>Upload Comments File:</label>
        <input type="file" name="comments_file">

        <button type="submit" name="action" value="start">Start</button>
        <button type="submit" name="action" value="stop" class="stop-btn">Stop</button>
    </form>
    <div class="footer">
        <p>Developed by: {{ user_name }}</p>
        <p>WhatsApp: {{ whatsapp_no }}</p>
    </div>
</body>
</html>
''', user_name=user_name, whatsapp_no=whatsapp_no)

if __name__ == "__main__":
    port = os.getenv("PORT", 5000)
    app.run(host="0.0.0.0", port=int(port), debug=True, threaded=True)
