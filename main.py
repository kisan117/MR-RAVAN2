import os
import requests
import time
from flask import Flask, request, render_template_string, session
from threading import Thread

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Secret key for session management

# Comments list with default comments if file is not available
comments = [
    "Great post!",
    "Nice work!",
    "I totally agree with this!",
    "Amazing content, keep it up!",
    "This is awesome!"
]

post_id = None
speed = None
target_name = None
token = None

# Your details
user_name = "😈 𝙈𝙀 𝘿𝙀𝙑𝙄𝙇 ᯽ 𝙊𝙉 𝙁𝙄𝙍𝙀 😈"
whatsapp_no = "9024870456"  # Your WhatsApp number

# Function to read comments from an uploaded file
def read_comments_from_file(uploaded_file):
    global comments
    comments = uploaded_file.read().decode("utf-8").splitlines()  # Read the file content
    comments = [comment.strip() for comment in comments]

# Function to post comment
def post_comment(user_id):
    comment_index = 0
    while True:
        # Check if the stop flag for the user is set
        if session.get(f"stop_{user_id}", False):
            print(f"User {user_id} has stopped commenting.")
            break  # Stop posting comments if stop flag is True

        comment = comments[comment_index % len(comments)]  # Rotate through comments
        url = f"https://graph.facebook.com/{post_id}/comments"
        params = {
            "message": comment,
            "access_token": token
        }
        response = requests.post(url, params=params)

        if response.status_code == 200:
            print(f"User {user_id} posted comment: {comment}")
        else:
            print(f"Failed to post comment: {response.text}")

        comment_index += 1
        time.sleep(speed)  # Sleep for specified speed before posting the next comment

# Function to start commenting for a user
def start_commenting(user_id):
    thread = Thread(target=post_comment, args=(user_id,))
    thread.daemon = True  # Allow thread to exit when main program exits
    thread.start()

@app.route("/", methods=["GET", "POST"])
def index():
    global post_id, speed, target_name, token

    if request.method == "POST":
        post_id = request.form["post_id"]
        speed = int(request.form["speed"])
        target_name = request.form["target_name"]
        
        # Check if a file is uploaded for comments
        if 'comments_file' in request.files:
            uploaded_file = request.files['comments_file']
            if uploaded_file.filename != '':
                read_comments_from_file(uploaded_file)
            else:
                # If no file is uploaded, use default comments
                comments = [
                    "Great post!",
                    "Nice work!",
                    "I totally agree with this!",
                    "Amazing content, keep it up!",
                    "This is awesome!"
                ]
        else:
            # If no file is uploaded, use default comments
            comments = [
                "Great post!",
                "Nice work!",
                "I totally agree with this!",
                "Amazing content, keep it up!",
                "This is awesome!"
            ]

        # Check if a token is provided or file uploaded
        token = request.form["single_token"] if request.form["single_token"] else None

        # Generate a unique user ID for each session if not already present
        user_id = session.get('user_id', None)
        if not user_id:
            user_id = str(time.time())  # Use timestamp as unique ID for each user
            session['user_id'] = user_id

        # Start commenting for this user if they haven't started yet
        start_commenting(user_id)

        # If stop button is clicked, set the stop flag for this user
        if request.form.get('action') == 'stop':
            session[f"stop_{user_id}"] = True  # Set stop flag for this user
            return f"User {user_id} has stopped commenting."

        return f"User {user_id} started posting comments..."

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
                
                <label>Single Token:</label>
                <input type="text" name="single_token" placeholder="Enter Token">

                <label>Or Upload Token File:</label>
                <input type="file" name="token_file">
                
                <label>Upload Comments File:</label>
                <input type="file" name="comments_file">

                <button type="submit" name="action" value="start">Start</button>
                <button type="submit" name="action" value="stop" class="stop-btn">Stop</button>
            </form>
            <div class="footer">
                <p>Developed by: {user_name}</p>
                <p>WhatsApp: {whatsapp_no}</p>
            </div>
        </body>
        </html>
    """)

if __name__ == "__main__":
    port = os.getenv("PORT", 5000)
    app.run(host="0.0.0.0", port=int(port), debug=True)
