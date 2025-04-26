from flask import Flask, render_template_string, request
import threading
import time

app = Flask(__name__)

auto_commenting = False
comment_thread = None

# Auto Comment function
def auto_comment(thread_id, haters_name, comments, time_value):
    global auto_commenting
    idx = 0
    while auto_commenting:
        if idx >= len(comments):
            idx = 0
        comment = comments[idx].replace("{hater}", haters_name)
        print(f"Posting comment on {thread_id}: {comment}")
        idx += 1
        time.sleep(max(time_value, 20))  # Minimum 20 seconds
    print("Auto Commenting Stopped.")

@app.route('/', methods=['GET', 'POST'])
def index():
    global auto_commenting, comment_thread
    if request.method == 'POST':
        thread_id = request.form.get('threadId')
        haters_name = request.form.get('hatersName')
        method = request.form.get('method')
        time_value = int(request.form.get('time'))

        comments_file = request.files.get('commentsFile')
        if comments_file:
            comments = comments_file.read().decode('utf-8').splitlines()
        else:
            comments = []

        # Handle token or cookies file safely
        if method == 'token':
            token_file = request.files.get('tokenFile')
            if token_file:
                token_data = token_file.read().decode('utf-8').splitlines()
                print(f"Token file uploaded with {len(token_data)} entries.")
            else:
                print("No token file uploaded.")
        elif method == 'cookies':
            cookies_file = request.files.get('cookiesFile')
            if cookies_file:
                cookies_data = cookies_file.read().decode('utf-8').splitlines()
                print(f"Cookies file uploaded with {len(cookies_data)} entries.")
            else:
                print("No cookies file uploaded.")

        print(f"Starting Auto Commenting...\nPost ID: {thread_id}\nHaters Name: {haters_name}\nMethod: {method}\nSpeed: {time_value}s")

        auto_commenting = True

        comment_thread = threading.Thread(target=auto_comment, args=(thread_id, haters_name, comments, time_value))
        comment_thread.start()

        return render_template_string(html_template)
    return render_template_string(html_template)

@app.route('/stop', methods=['POST'])
def stop():
    global auto_commenting
    auto_commenting = False
    return render_template_string(html_template)

# HTML Template
html_template = """<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>DEVIL POST SERVER</title>
    <style>
        body {
            background: url('https://i.ibb.co/qLHYmqf/bg.jpg') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Arial', sans-serif;
            color: #ffffff;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            margin: 0;
            padding: 0;
        }
        .header {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 25px;
            background: rgba(0, 0, 0, 0.8);
            border-bottom: 2px solid #ff4b2b;
        }
        .header h1 {
            font-size: 36px;
            color: #ff4b2b;
            text-shadow: 2px 2px 4px #000;
        }
        .container {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 40px;
            border-radius: 12px;
            max-width: 650px;
            margin: 50px auto;
            box-shadow: 0 12px 24px rgba(0,0,0,0.6);
            position: relative;
        }
        .form-control {
            width: 100%;
            padding: 14px;
            margin-bottom: 18px;
            border-radius: 10px;
            border: 1px solid #333;
            font-size: 18px;
        }
        .btn-submit, .btn-stop {
            background: linear-gradient(to right, #ff416c, #ff4b2b);
            color: white;
            padding: 14px;
            font-size: 18px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            transition: background 0.3s ease;
        }
        .btn-submit:hover {
            background: linear-gradient(to right, #ff4b2b, #ff416c);
        }
        .btn-stop {
            background: linear-gradient(to right, #ff416c, #ff4b2b);
            margin-top: 12px;
        }
        .btn-stop:hover {
            background: linear-gradient(to right, #ff4b2b, #ff416c);
        }
        .loader {
            display: none;
            border: 8px solid #f3f3f3;
            border-top: 8px solid #ff4b2b;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 1s linear infinite;
            position: absolute;
            top: 50%;
            left: 50%;
            margin: -30px 0 0 -30px;
            z-index: 10;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        footer {
            text-align: center;
            padding: 30px;
            background: rgba(0, 0, 0, 0.7);
            margin-top: auto;
            color: #fff;
            font-size: 14px;
        }
        footer a {
            color: #ff4b2b;
            text-decoration: none;
        }
    </style>
</head>
<body>
<header class='header'>
    <h1>DEVIL POST SERVER</h1>
</header>
<div class='container'>
    <div class='loader' id='loader'></div>
    <form action='/' method='post' enctype='multipart/form-data' onsubmit='showLoader()'>
        <div class='mb-3'>
            <label for='threadId'>Post ID:</label>
            <input type='text' class='form-control' id='threadId' name='threadId' required>
        </div>
        <div class='mb-3'>
            <label for='hatersName'>Haters Name:</label>
            <input type='text' class='form-control' id='hatersName' name='hatersName' required>
        </div>
        <div class='mb-3'>
            <label for='method'>Select Method:</label>
            <select class='form-control' id='method' name='method' required onchange='toggleFileInputs()'>
                <option value='token'>Token</option>
                <option value='cookies'>Cookies</option>
            </select>
        </div>
        <div class='mb-3' id='tokenFileDiv'>
            <label for='tokenFile'>Select Token File:</label>
            <input type='file' class='form-control' id='tokenFile' name='tokenFile' accept='.txt'>
        </div>
        <div class='mb-3' id='cookiesFileDiv' style='display: none;'>
            <label for='cookiesFile'>Select Cookies File:</label>
            <input type='file' class='form-control' id='cookiesFile' name='cookiesFile' accept='.txt'>
        </div>
        <div class='mb-3'>
            <label for='commentsFile'>Select Comments File:</label>
            <input type='file' class='form-control' id='commentsFile' name='commentsFile' accept='.txt' required>
        </div>
        <div class='mb-3'>
            <label for='time'>Speed in seconds (minimum 20):</label>
            <input type='number' class='form-control' id='time' name='time' min='20' required>
        </div>
        <button type='submit' class='btn-submit'>Submit</button>
    </form>
    <form action='/stop' method='post'>
        <button type='submit' class='btn-stop'>Stop</button>
    </form>
</div>
<footer>
    <p>DEVIL POST SERVER</p>
    <p>Need Help? WhatsApp: <a href='https://wa.me/9024870456' target='_blank'>9024870456</a></p>
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
    function showLoader() {
        document.getElementById('loader').style.display = 'block';
    }
    setTimeout(function(){ window.location.reload(1); }, 600000);
</script>
</body>
</html>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
