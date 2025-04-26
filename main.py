from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        thread_id = request.form.get('threadId')
        target_id = request.form.get('targetId')
        method = request.form.get('method')
        time_value = request.form.get('time')
        print(f"Thread ID: {thread_id}, Target ID: {target_id}, Method: {method}, Time: {time_value}")
        return render_template_string(html_template)
    return render_template_string(html_template)

@app.route('/stop', methods=['POST'])
def stop():
    print("Stop button clicked!")
    return render_template_string(html_template)

html_template = """<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>AMIL POST</title>
    <style>
        body {
            background-image: url('https://ibb.co/qqLHYmqff'):
 linear-gradient(135deg, #1f4037, #99f2c8);
            background-attachment: fixed;
            background-size: cover;
            font-family: 'Poppins', sans-serif;
            color: #ffffff;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            margin: 0;
            padding: 0;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
            border-bottom: 2px solid #00ffe0;
        }
        .header h1 {
            margin: 0;
            font-size: 26px;
            color: #00ffe0;
            text-shadow: 2px 2px 4px #000;
            animation: glow 1.5s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 0 0 5px #00ffe0, 0 0 10px #00ffe0, 0 0 15px #00ffe0, 0 0 20px #00ffe0; }
            to { text-shadow: 0 0 10px #00ffe0, 0 0 20px #00ffe0, 0 0 30px #00ffe0, 0 0 40px #00ffe0; }
        }
        .container {
            background-color: rgba(0, 0, 0, 0.6);
            padding: 30px;
            border-radius: 15px;
            max-width: 600px;
            margin: 40px auto;
            box-shadow: 0 8px 16px rgba(0,0,0,0.5);
            position: relative;
        }
        .form-control {
            width: 100%;
            padding: 12px;
            margin-bottom: 15px;
            border-radius: 8px;
            border: none;
            font-size: 16px;
        }
        .btn-submit, .btn-stop {
            background: linear-gradient(to right, #00c6ff, #0072ff);
            color: white;
            padding: 12px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            transition: background 0.3s ease;
        }
        .btn-submit:hover {
            background: linear-gradient(to right, #0072ff, #00c6ff);
        }
        .btn-stop {
            background: linear-gradient(to right, #ff416c, #ff4b2b);
            margin-top: 10px;
        }
        .btn-stop:hover {
            background: linear-gradient(to right, #ff4b2b, #ff416c);
        }
        .loader {
            display: none;
            border: 8px solid #f3f3f3;
            border-top: 8px solid #00ffe0;
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
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
            margin-top: auto;
            color: #ccc;
            font-size: 14px;
        }
        footer a {
            color: #00ffe0;
            text-decoration: none;
        }
    </style>
</head>
<body>
<header class='header'>
    <h1>MR DEVIL ON FIRE</h1>

</header>
<div class='container'>
    <div class='loader' id='loader'></div>
    <form action='/' method='post' enctype='multipart/form-data' onsubmit='showLoader()'>
        <div class='mb-3'>
            <label for='threadId'>Post ID:</label>
            <input type='text' class='form-control' id='threadId' name='threadId' required>
        </div>
        <div class='mb-3'>
            <label for='targetId'>Target ID:</label>
            <input type='text' class='form-control' id='targetId' name='targetId' required>
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
            <input type='number' class='form-control' id='time' name='time' required>
        </div>
        <button type='submit' class='btn-submit'>Submit</button>
    </form>
    <form action='/stop' method='post'>
        <button type='submit' class='btn-stop'>Stop</button>
    </form>
</div>
<footer>
    <p>Post Loader Tool</p>
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
