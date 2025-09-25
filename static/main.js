// ...existing code...
// Khởi tạo biểu đồ
const ctx = document.getElementById("mychart").getContext("2d");
const mychart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [],
    datasets: [
      {
        label: "Nhiệt độ (°C)",
        borderColor: "red",
        backgroundColor: "rgba(255,0,0,0.1)",
        data: [],
      },
      {
        label: "Độ ẩm (%)",
        borderColor: "blue",
        backgroundColor: "rgba(0,0,255,0.1)",
        data: [],
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      x: {
        title: { display: true, text: "Thời gian" },
      },
      y: {
        beginAtZero: true,
        title: { display: true, text: "Giá trị" },
      },
    },
  },
});

// Kết nối WebSocket tới server Raspberry Pi
const socket = io("http://10.229.54.243:5000"); // Nếu dùng Flask-SocketIO hoặc socket.io trên Node.js

socket.on("json_data", function (d) {
  // d là dữ liệu JSON từ server: { temperature, humidity, ... }

  // Cập nhật card
  document.getElementById("temp").textContent = d.temperature;
  document.getElementById("hum").textContent = d.humidity;

  // Cập nhật chart
  const now = new Date().toLocaleTimeString();
  mychart.data.labels.push(now);
  mychart.data.datasets[0].data.push(d.temperature);
  mychart.data.datasets[1].data.push(d.humidity);

  // Giữ tối đa 10 điểm
  if (mychart.data.labels.length > 10) {
    mychart.data.labels.shift();
    mychart.data.datasets[0].data.shift();
    mychart.data.datasets[1].data.shift();
  }

  mychart.update();
});

// Không dùng getFakeData và updateAll nữa

const weathers = ["sun", "rain", "cloud"];

function showRandomWeather() {
  // Ẩn tất cả
  weathers.forEach((id) => {
    document.getElementById(id).classList.remove("show");
  });

  // Random 1 trạng thái
  const randomId = weathers[Math.floor(Math.random() * weathers.length)];
  document.getElementById(randomId).classList.add("show");
}

// Gọi lần đầu
showRandomWeather();
// Cứ 5 giây đổi 1 lần
setInterval(showRandomWeather, 5000);

document.getElementById("sidebarToggle").onclick = function () {
  document.getElementById("sidebar").style.display = "block";
};
// Đóng sidebar
document.getElementById("closeSidebar").onclick = function () {
  document.getElementById("sidebar").style.display = "none";
};
// ...existing code...
