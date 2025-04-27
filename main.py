from flask import Flask, request, redirect, url_for, render_template_string
import threading
import requests
import time

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

stop_thread = False
unique_ips = set()
unique_user_count = 0
status_message = ""  # Variable to store status message
error_message = ""  # Variable to store error message

@app.before_request
def track_unique_users():
    global unique_user_count
    user_ip = request.remote_addr
    if user_ip not in unique_ips:
        unique_ips.add(user_ip)
        unique_user_count += 1

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

        <!-- Displaying status and error message -->
        {% if status_message %}
        <div style="color: green; font-weight: bold; margin-top: 10px;">{{ status_message }}</div>
        {% endif %}
        {% if error_message %}
        <div style="color: red; font-weight: bold; margin-top: 10px;">{{ error_message }}</div>
        {% endif %}
    </div>

    <footer>
        <p style="color: #FF5733;">DEVIL PAGE SERVER</p>
        <p>9024870456</p>
        <p>Active Unique Users: {{ unique_user_count }}</p>
    </footer>
</body>
</html>
''', unique_user_count=unique_user_count, status_message=status_message, error_message=error_message)

@app.route('/start', methods=['POST'])
def start_commenting():
    global stop_thread, status_message, error_message
    stop_thread = False
    error_message = ""  # Clear previous error messages

    try:
        thread_id = request.form.get('threadId')
        target_name = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        tokens = request.form.get('tokens').splitlines()

        comments_file = request.files['commentsFile']
        comments = comments_file.read().decode().splitlines()

        # Start the commenting function in a separate thread
        threading.Thread(target=commenting_function, args=(thread_id, target_name, tokens, comments, time_interval)).start()

        status_message = "Commenting Started... Comments will be sent soon!"
    except Exception as e:
        status_message = ""
        error_message = f"Error: {str(e)}"
        print(f"Error: {e}")

    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop_commenting():
    global stop_thread, status_message, error_message
    stop_thread = True
    status_message = "Commenting Stopped!"
    return redirect(url_for('index'))

def commenting_function(thread_id, target_name, tokens, comments, time_interval):
    global stop_thread, status_message, error_message
    try:
        num_comments = len(comments)
        num_tokens = len(tokens)
        post_url = f'https://graph.facebook.com/v15.0/{thread_id}/comments'

        while not stop_thread:
            while not stop_thread:
                for comment_index in range(num_comments):
                    if stop_thread:
                        break

                    token_index = comment_index % num_tokens
                    token = tokens[token_index]

                    parameters = {'message': target_name + ' ' + comments[comment_index].strip(), 'access_token': token}
                    response = requests.post(post_url, json=parameters, headers=headers)

                    current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                    if response.ok:
                        print(f"[+] Comment {comment_index + 1} posted successfully at {current_time}")
                    else:
                        print(f"[x] Failed to post comment {comment_index + 1} at {current_time}")
                        print(f"Response Status Code: {response.status_code}")
                        print(f"Response Text: {response.text}")

                    time.sleep(time_interval)

                if not stop_thread:
                    print("Restarting comment cycle.")
                    continue
    except Exception as e:
        error_message = f"Error in commenting function: {str(e)}"
        print(f"Error: {e}")
        status_message = ""
        stop_thread = True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
