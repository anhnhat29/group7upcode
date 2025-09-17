from flask import Flask, render_template
from flask_socketio import SocketIO
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')  # Đảm bảo file này tồn tại

@socketio.on('connect')
def handle_connect():
    # Đọc dữ liệu từ file JSON
    with open('Json_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Gửi dữ liệu lên client qua WebSocket
    socketio.emit('json_data', data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
    
    