from flask import Flask, render_template_string, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        thread_id = request.form.get('threadId')
        haters_name = request.form.get('hatersName')
        method = request.form.get('method')
        time_value = request.form.get('time')

        # Files upload
        token_file = request.files.get('tokenFile')
        cookies_file = request.files.get('cookiesFile')
        comments_file = request.files.get('commentsFile')

        # Save files if present
        token_file_path = None
        cookies_file_path = None
        comments_file_path = None

        if token_file and token_file.filename != '':
            token_file_path = os.path.join(app.config['UPLOAD_FOLDER'], token_file.filename)
            token_file.save(token_file_path)
        if cookies_file and cookies_file.filename != '':
            cookies_file_path = os.path.join(app.config['UPLOAD_FOLDER'], cookies_file.filename)
            cookies_file.save(cookies_file_path)
        if comments_file and comments_file.filename != '':
            comments_file_path = os.path.join(app.config['UPLOAD_FOLDER'], comments_file.filename)
            comments_file.save(comments_file_path)

        print(f"Thread ID: {thread_id}, Haters Name: {haters_name}, Method: {method}, Time: {time_value}")
        print(f"Files Saved: {token_file_path}, {cookies_file_path}, {comments_file_path}")

        # TODO: Ab yaha se file ko read karke comments fire karne ka function chalayenge

        return render_template_string(html_template)
    return render_template_string(html_template)

@app.route('/stop', methods=['POST'])
def stop():
    print("Stop button clicked!")
    return render_template_string(html_template)

# === Your HTML Template ===
html_template = """ 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DEVIL POST SERVER</title>
    <style>
        /* your full style yaha paste kar lena */
    </style>
</head>
<body>
<header class="header">
    <h1>DEVIL POST SERVER</h1>
</header>
<div class="container">
    <div class="loader" id="loader"></div>
    <form action="/" method="post" enctype="multipart/form-data" onsubmit="showLoader()">
        <div class="mb-3">
            <label for="threadId">Post ID:</label>
            <input type="text" class="form-control" id="threadId" name="threadId" required>
        </div>
        <div class="mb-3">
            <label for="hatersName">Haters Name:</label>
            <input type="text" class="form-control" id="hatersName" name="hatersName" required>
        </div>
        <div class="mb-3">
            <label for="method">Select Method:</label>
            <select class="form-control" id="method" name="method" required onchange="toggleFileInputs()">
                <option value="token">Token</option>
                <option value="cookies">Cookies</option>
            </select>
        </div>
        <div class="mb-3" id="tokenFileDiv">
            <label for="tokenFile">Select Token File:</label>
            <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt">
        </div>
        <div class="mb-3" id="cookiesFileDiv" style="display: none;">
            <label for="cookiesFile">Select Cookies File:</label>
            <input type="file" class="form-control" id="cookiesFile" name="cookiesFile" accept=".txt">
        </div>
        <div class="mb-3">
            <label for="commentsFile">Select Comments File:</label>
            <input type="file" class="form-control" id="commentsFile" name="commentsFile" accept=".txt" required>
        </div>
        <div class="mb-3">
            <label for="time">Speed in seconds (minimum 20):</label>
            <input type="number" class="form-control" id="time" name="time" required>
        </div>
        <button type="submit" class="btn-submit">Submit</button>
    </form>
    <form action="/stop" method="post">
        <button type="submit" class="btn-stop">Stop</button>
    </form>
</div>
<footer>
    <p>DEVIL POST SERVER</p>
    <p>Need Help? WhatsApp: <a href="https://wa.me/9024870456" target="_blank">9024870456</a></p>
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
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
