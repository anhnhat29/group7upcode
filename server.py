from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import paho.mqtt.client as paho
from paho import mqtt

app = Flask(__name__)
socketio = SocketIO(app)

# ===== Flask routes =====
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    try:
        with open('json_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        emit('json_data', data)
    except Exception as e:
        emit('json_data', {"error": str(e)})


# ===== MQTT setup =====
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("anhnhat", "Sn29022004")
client.connect("9c36c11f80b147c09427b67db165c3b7.s1.eu.hivemq.cloud", 8883)
client.subscribe("test/esp", qos=1)

# Hàm xử lý khi có tin nhắn MQTT
def on_message(client, userdata, message):
    try:
        # Giải mã dữ liệu
        payload = message.payload.decode("utf-8")
        data = json.loads(payload)

        # Lưu vào file JSON
        with open("json_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print("Đã nhận dữ liệu:", data)

        # Gửi realtime lên web qua SocketIO
        socketio.emit('json_data', data)

    except Exception as e:
        print("Lỗi xử lý dữ liệu:", e)

client.on_message = on_message

# == code của nhật===============
if __name__ == '__main__':
    # Cho MQTT chạy nền
    client.loop_start()

    # Chạy Flask
    socketio.run(app, host='0.0.0.0', port=5000)
#== end code của nhật===============