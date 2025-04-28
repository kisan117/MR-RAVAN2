from flask import Flask, request, jsonify
import requests
import random
import time
import threading

app = Flask(__name__)

# Facebook API URL for posting comments
API_URL = 'https://graph.facebook.com/v15.0/{thread_id}/comments'
# List of Facebook access tokens (replace with your valid tokens)
tokens = ['YOUR_TOKEN_1', 'YOUR_TOKEN_2', 'YOUR_TOKEN_3']

# Global flag to manage stop button
stop_thread = {}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
}

@app.route('/post_comments', methods=['POST'])
def post_comments():
    data = request.form

    thread_id = data.get('thread_id')
    speed = int(data.get('speed', 20))  # Default to 20 seconds if not specified
    
    if not thread_id:
        return jsonify({"error": "Missing thread_id"}), 400

    # Check if file is uploaded
    if 'comments_file' not in request.files:
        return jsonify({"error": "Missing comments file"}), 400

    comments_file = request.files['comments_file']
    comments = comments_file.read().decode().splitlines()  # Read comments from file

    # Start the commenting process
    threading.Thread(target=post_comments_to_thread, args=(thread_id, comments, speed)).start()

    return jsonify({"message": "Comments are being posted successfully!"}), 200


def post_comments_to_thread(thread_id, comments, interval):
    total_comments_sent = 0
    comment_index = 0
    retry_attempts = 0  # Retry attempts counter

    while True:  # Infinite loop to keep posting comments
        if stop_thread.get(thread_id, False):  # Stop condition for thread
            print("Stopping comment posting...")
            break

        # Choose a random token
        token = random.choice(tokens)
        comment = comments[comment_index % len(comments)]  # Loop through comments
        comment_index += 1

        # Prepare request payload
        payload = {'message': comment, 'access_token': token}

        try:
            # Send POST request to Facebook API
            response = requests.post(API_URL.format(thread_id=thread_id), json=payload, headers=headers)

            if response.ok:
                total_comments_sent += 1
                print(f"Comment {total_comments_sent} posted successfully.")
                retry_attempts = 0  # Reset retry attempts after a successful comment
            else:
                print(f"Error posting comment: {response.status_code}, {response.text}")
                if retry_attempts < 3:  # Retry 3 times if the comment fails
                    retry_attempts += 1
                    print(f"Retrying... Attempt {retry_attempts}")
                    time.sleep(10)  # Wait before retrying
                    continue
                else:
                    print("Max retry attempts reached. Skipping this comment.")
                    retry_attempts = 0

        except requests.exceptions.RequestException as e:
            print(f"Error posting comment: {e}")
            time.sleep(10)  # Wait for 10 seconds before retrying

        time.sleep(interval)  # Wait for the interval before posting the next comment


@app.route('/stop', methods=['POST'])
def stop_commenting():
    # Set stop flag to True
    stop_thread['thread_id'] = True
    return jsonify({"message": "Comment posting has been stopped!"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
