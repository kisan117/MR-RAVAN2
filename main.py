from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Auto Comment System is Running!"

@app.route('/submit', methods=['POST'])
def submit():
    hater_name = request.form.get('hater_name')
    if not hater_name:
        return jsonify({'error': 'Hater Name is required'}), 400
    with open('hater_name.txt', 'w') as f:
        f.write(hater_name)
    return jsonify({'message': f'Hater Name {hater_name} saved successfully'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
