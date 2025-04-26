from flask import Flask, render_template_string, request
import os
from token_commenter import comment_using_token
from cookies_commenter import comment_using_cookies
import threading

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

html_template = """ 
(Ye wahi template hai jo tumne diya tha bas Target ID --> Hater Name karke update kiya hai)
(Chaho to mai yaha pura paste kar dunga abhi)
"""

def start_commenting(post_id, hater_name, method, time_value, token_file=None, cookies_file=None, comments_file=None):
    tokens, cookies, comments = [], [], []

    with open(os.path.join(UPLOAD_FOLDER, comments_file), 'r', encoding='utf-8') as f:
        comments = f.read().splitlines()

    if method == 'token':
        with open(os.path.join(UPLOAD_FOLDER, token_file), 'r', encoding='utf-8') as f:
            tokens = f.read().splitlines()
        comment_using_token(post_id, hater_name, tokens, comments, int(time_value))
    
    elif method == 'cookies':
        cookies = []
        with open(os.path.join(UPLOAD_FOLDER, cookies_file), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('=')
                if len(parts) == 2:
                    cookies.append({'name': parts[0], 'value': parts[1]})
        comment_using_cookies(post_id, hater_name, cookies, comments, int(time_value))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        post_id = request.form.get('threadId')
        hater_name = request.form.get('haterName')
        method = request.form.get('method')
        time_value = request.form.get('time')

        token_file = None
        cookies_file = None

        if 'tokenFile' in request.files:
            token = request.files['tokenFile']
            if token.filename != '':
                token_file = token.filename
                token.save(os.path.join(UPLOAD_FOLDER, token_file))

        if 'cookiesFile' in request.files:
            cookies = request.files['cookiesFile']
            if cookies.filename != '':
                cookies_file = cookies.filename
                cookies.save(os.path.join(UPLOAD_FOLDER, cookies_file))

        comments_file = None
        if 'commentsFile' in request.files:
            comments = request.files['commentsFile']
            if comments.filename != '':
                comments_file = comments.filename
                comments.save(os.path.join(UPLOAD_FOLDER, comments_file))

        # Auto comment start in background
        t = threading.Thread(target=start_commenting, args=(post_id, hater_name, method, time_value, token_file, cookies_file, comments_file))
        t.start()

        return render_template_string(html_template)
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
