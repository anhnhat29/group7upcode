from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index2.html')

@socketio.on('connect')
def handle_connect():
    try:
        with open('json_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        emit('json_data', data)
    except Exception as e:
        emit('json_data', {"error": str(e)})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)