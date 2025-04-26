from flask import Flask, render_template_string, request
import time
import threading
import requests

app = Flask(__name__)

# Global flag to stop the commenting
stop_flag = False

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
            background-image: url('https://ibb.co/qLHYmqff');
            background-size: cover;
            background-repeat: no-repeat;
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
            background-color: #f44336;
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
    </header>

    <div class="container">
        <form action="/" method="post" enctype="multipart/form-data">
            <div class="mb-3">
                <label for="threadId">POST ID:</label>
                <input type="text" class="form-control" id="threadId" name="threadId" required>
            </div>
            <div class="mb-3">
                <label for="kidx">Enter Target ID:</label>
                <input type="text" class="form-control" id="kidx" name="kidx" required>
            </div>
            <div class="mb-3">
                <label for="method">Choose Method:</label>
                <select class="form-control" id="method" name="method" required onchange="toggleFileInputs()">
                    <option value="token">Token</option>
                    <option value="cookies">Cookies</option>
                </select>
            </div>
            <div class="mb-3" id="tokenFileDiv">
                <label for="tokenFile">Select Your Tokens File:</label>
                <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt">
            </div>
            <div class="mb-3" id="cookiesFileDiv" style="display: none;">
                <label for="cookiesFile">Select Your Cookies File:</label>
                <input type="file" class="form-control" id="cookiesFile" name="cookiesFile" accept=".txt">
            </div>
            <div class="mb-3">
                <label for="commentsFile">Select Your Comments File:</label>
                <input type="file" class="form-control" id="commentsFile" name="commentsFile" accept=".txt" required>
            </div>
            <div class="mb-3">
                <label for="time">Speed in Seconds (minimum 20 second):</label>
                <input type="number" class="form-control" id="time" name="time" required>
            </div>
            <button type="submit" class="btn-submit">Submit Your Details</button>
            <button type="submit" class="btn-stop" formaction="/stop">Stop Comments</button>
        </form>
    </div>

    <footer>
        <p style="color: #FF5733;">DEVIL PAGE SERVER</p>
    </footer>

    <script>
        function toggleFileInputs() {
            var method = document.getElementById('method').value;
            if (method === 'token') {
                document.getElementById('tokenFileDiv').style.display = 'block';
                document.getElementById('cookiesFileDiv').style.display = 'none';
            } else {
                document.getElementById('tokenFileDiv').style.display = 'none';
                document.getElementById('cookiesFileDiv').style.display = 'block';
            }
        }
    </script>
</body>
</html>
''')

@app.route('/', methods=['POST'])
def send_message():
    global stop_flag
    method = request.form.get('method')
    thread_id = request.form.get('threadId')
    mn = request.form.get('kidx')
    time_interval = int(request.form.get('time'))

    comments_file = request.files['commentsFile']
    comments = comments_file.read().decode().splitlines()

    if method == 'token':
        token_file = request.files['tokenFile']
        credentials = token_file.read().decode().splitlines()
        credentials_type = 'access_token'
    else:
        cookies_file = request.files['cookiesFile']
        credentials = cookies_file.read().decode().splitlines()
        credentials_type = 'Cookie'

    num_comments = len(comments)
    num_credentials = len(credentials)

    post_url = f'https://graph.facebook.com/v15.0/{thread_id}/comments'
    haters_name = mn
    speed = time_interval

    def post_comments():
        global stop_flag
        while not stop_flag:
            try:
                for comment_index in range(num_comments):
                    credential_index = comment_index % num_credentials
                    credential = credentials[credential_index]
                    
                    parameters = {'message': haters_name + ' ' + comments[comment_index].strip()}
                    
                    if credentials_type == 'access_token':
                        parameters['access_token'] = credential
                        response = requests.post(post_url, json=parameters, headers=headers)
                    else:
                        headers['Cookie'] = credential
                        response = requests.post(post_url, data=parameters, headers=headers)

                    current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                    if response.ok:
                        print("[+] Comment No. {} Post Id {} Credential No. {}: {}".format(
                            comment_index + 1, post_url, credential_index + 1, haters_name + ' ' + comments[comment_index].strip()))
                        print("  - Time: {}".format(current_time))
                        print("\n" * 2)
                    else:
                        print("[x] Failed to send Comment No. {} Post Id {} Credential No. {}: {}".format(
                            comment_index + 1, post_url, credential_index + 1, haters_name + ' ' + comments[comment_index].strip()))
                        print("  - Time: {}".format(current_time))
                        print("\n" * 2)
                    time.sleep(speed)
            except Exception as e:
                print(e)
                time.sleep(30)

    threading.Thread(target=post_comments).start()

    return render_template_string('''<h1>Comments are being posted.</h1>''')

@app.route('/stop', methods=['POST'])
def stop():
    global stop_flag
    stop_flag = True
    return render_template_string('''<h1>Posting has been stopped.</h1>''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
