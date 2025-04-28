import os
import requests
import schedule
import time
from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML Template (same as before)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Auto Comment Bot</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f0f0; text-align: center; }
        form { background: white; padding: 20px; margin: auto; width: 300px; margin-top: 50px; border-radius: 10px; box-shadow: 0px 0px 10px grey; }
        input, button { width: 100%; padding: 10px; margin: 10px 0; }
        button { background: green; color: white; border: none; cursor: pointer; }
        .stop-btn { background: red; }
    </style>
</head>
<body>
    <h2>Facebook Auto Comment Bot</h2>
    <form action="/" method="post" enctype="multipart/form-data">
        <input type="text" name="post_id" placeholder="Enter Post ID" required>
        <input type="text" name="speed" placeholder="Enter Speed (seconds)" required>
        <input type="text" name="target_name" placeholder="Enter Target Name" required>
        
        <label>Single Token:</label>
        <input type="text" name="single_token" placeholder="Enter Token">

        <label>Or Upload Token File:</label>
        <input type="file" name="token_file">
        
        <label>Upload Cookies File:</label>
        <input type="file" name="cookies_file">

        <label>Upload Comments File:</label>
        <input type="file" name="comments_file">

        <button type="submit" name="action" value="start">Start</button>
        <button type="submit" name="action" value="stop" class="stop-btn">Stop</button>
    </form>
</body>
</html>
"""

# Global variables
token = None
post_id = None
speed = None
target_name = None
comments = []

# Function to simulate posting a comment
def post_comment():
    if token and post_id and target_name:
        comment = f"Hey {target_name}, this is an automated comment!"
        url = f"https://graph.facebook.com/{post_id}/comments"
        params = {
            "message": comment,
            "access_token": token
        }
        response = requests.post(url, params=params)

        if response.status_code == 200:
            print("✅ Comment posted successfully!")
        else:
            print(f"❌ Failed to post comment: {response.text}")

def start_commenting():
    global post_id, speed, target_name, token
    while True:
        post_comment()
        time.sleep(speed)

@app.route("/", methods=["GET", "POST"])
def index():
    global post_id, speed, target_name, token
    if request.method == "POST":
        post_id = request.form["post_id"]
        speed = int(request.form["speed"])
        target_name = request.form["target_name"]
        
        # Check if a token is provided or file uploaded
        token = request.form["single_token"] if request.form["single_token"] else None
        
        if request.form["action"] == "start":
            # Start the commenting loop with a new thread
            from threading import Thread
            thread = Thread(target=start_commenting)
            thread.start()
            return "✅ Commenting started!"
        
        if request.form["action"] == "stop":
            # Logic to stop commenting (This could involve terminating the thread or adding a stop flag)
            return "❌ Commenting stopped!"

    return render_template_string(HTML_TEMPLATE)

# Run Flask app
if __name__ == "__main__":
    port = os.getenv("PORT", 5000)
    app.run(host="0.0.0.0", port=int(port), debug=True)
