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

// Hàm sinh dữ liệu giả
function getFakeData() {
  return {
    temperature: (20 + Math.random() * 10).toFixed(1), // 20–30 °C
    humidity: (40 + Math.random() * 40).toFixed(1), // 40–80 %
  };
}

// Hàm cập nhật card + chart
function updateAll() {
  const d = getFakeData();

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
}

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

// Chạy lần đầu và lặp lại mỗi 2 giây
updateAll();
setInterval(updateAll, 2000);
