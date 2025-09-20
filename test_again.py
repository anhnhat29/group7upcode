import paho.mqtt.client as mqtt
import json
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Thiết lập Flask và Flask-SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# MQTT client callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe vào topic mà ESP32 sẽ gửi dữ liệu
    client.subscribe("esp32/sensor/data")  # Thay "esp32/sensor/data" bằng topic thật mà ESP32 sử dụng

def on_message(client, userdata, msg):
    print(f"Data received: {msg.payload.decode()}")
    try:
        # Chuyển đổi dữ liệu từ dạng byte sang JSON
        data = json.loads(msg.payload.decode())
        # Gửi dữ liệu qua WebSocket cho giao diện web
        socketio.emit('json_data', data)
    except Exception as e:
        print(f"Error parsing message: {e}")

# Tạo MQTT client và kết nối
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Kết nối đến broker MQTT (thay bằng địa chỉ broker của bạn)
client.connect("broker_address", 1883, 60)

# Định nghĩa route cho Flask (giao diện web)
@app.route('/')
def index():
    return render_template('index.html')  # Đảm bảo có file index.html trong thư mục templates

if __name__ == '__main__':
    # Bắt đầu nhận dữ liệu MQTT
    client.loop_start()  # Bắt đầu vòng lặp để nhận dữ liệu từ ESP32 qua MQTT
    # Chạy Flask và WebSocket
    socketio.run(app, host='0.0.0.0', port=5000)
