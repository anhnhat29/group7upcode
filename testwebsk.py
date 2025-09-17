from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.htmml')  # Đảm bảo file này tồn tại

@socketio.on('connect')
def handle_connect():
    with open('Json_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    emit('json_data', data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
    