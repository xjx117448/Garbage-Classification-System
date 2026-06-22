import sys
import os
import cv2
import time
import torch
import datetime
from openpyxl import Workbook

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# =========================
# Loading窗口（新增）
# =========================
class LoadingWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("系统启动中")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.resize(420, 140)

        self.label = QLabel("正在加载模型...", self)
        self.label.setAlignment(Qt.AlignCenter)

        self.bar = QProgressBar(self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.bar)
        self.setLayout(layout)

        self.value = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_bar)

    def start(self):
        self.show()
        self.timer.start(30)

    def update_bar(self):
        self.value += 3
        self.bar.setValue(self.value)

        if self.value >= 100:
            self.timer.stop()
            self.close()


# =========================
# 主GUI（完全保留你的功能）
# =========================
class GarbageGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("智能垃圾分类识别系统 V3.1")

        # ✔ ICON（新增）
        self.setWindowIcon(QIcon(r"C:\Users\sdbydhk\yolov5-master\garbage_system\icon\icon.ico"))

        self.resize(1500, 900)

        # ✔ 输出目录统一（新增）
        self.result_dir = r"C:\Users\sdbydhk\yolov5-master\garbage_system\result"
        os.makedirs(self.result_dir, exist_ok=True)

        self.image_path = None
        self.cap = None
        self.last_time = time.time()
        self.history = []

        self.load_model()
        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_camera)

    # ---------------- MODEL ----------------
    def load_model(self):
        weight_path = os.path.join(os.path.dirname(__file__), "weights", "garbage_v1_best.pt")

        self.model = torch.hub.load(
            '..',
            'custom',
            path=weight_path,
            source='local'
        )

        self.names = self.model.names

        self.cls_map = {
            "recyclable_waste": "可回收垃圾",
            "kitchen_waste": "厨余垃圾",
            "hazardous_waste": "有害垃圾",
            "other_waste": "其他垃圾"
        }

    # ---------------- UI（完全不删） ----------------
    def init_ui(self):

        title = QLabel("♻ YOLOv5 智能垃圾分类系统")
        title.setAlignment(Qt.AlignCenter)

        self.btn_img = QPushButton("📁 图片检测")
        self.btn_det = QPushButton("🔍 开始检测")
        self.btn_cam = QPushButton("📷 摄像头")
        self.btn_stop = QPushButton("⛔ 停止")
        self.btn_clear = QPushButton("🗑 清空")
        self.btn_export = QPushButton("📊 导出Excel")

        for b in [self.btn_img, self.btn_det, self.btn_cam, self.btn_stop, self.btn_clear, self.btn_export]:
            b.setMinimumHeight(40)

        self.btn_img.clicked.connect(self.load_image)
        self.btn_det.clicked.connect(self.detect_image)
        self.btn_cam.clicked.connect(self.start_camera)
        self.btn_stop.clicked.connect(self.stop_camera)
        self.btn_clear.clicked.connect(self.clear_all)
        self.btn_export.clicked.connect(self.export_excel)

        self.label_left = QLabel("原图")
        self.label_right = QLabel("检测结果")

        self.label_left.setAlignment(Qt.AlignCenter)
        self.label_right.setAlignment(Qt.AlignCenter)

        self.time_label = QLabel("0.000s")
        self.fps_label = QLabel("0")
        self.total_label = QLabel("0")
        self.rec_label = QLabel("0")
        self.kit_label = QLabel("0")
        self.haz_label = QLabel("0")
        self.oth_label = QLabel("0")

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        self.status = QLabel("模型状态：已加载 | V3.1")

        layout = QVBoxLayout()
        layout.addWidget(title)

        btn = QHBoxLayout()
        for i in [self.btn_img, self.btn_det, self.btn_cam, self.btn_stop, self.btn_clear, self.btn_export]:
            btn.addWidget(i)

        layout.addLayout(btn)

        img = QHBoxLayout()
        img.addWidget(self.label_left)
        img.addWidget(self.label_right)

        layout.addLayout(img)
        layout.addWidget(self.result_text)
        layout.addWidget(self.status)

        self.setLayout(layout)

    # ---------------- IMAGE ----------------
    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择图片")
        if path:
            self.image_path = path
            self.show_img(path, self.label_left)

    def show_img(self, path, label):
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = img.shape
        q = QImage(img.data, w, h, c*w, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(q).scaled(label.size(), Qt.KeepAspectRatio))

    # ---------------- DETECT ----------------
    def detect_image(self):

        if not self.image_path:
            return

        start = time.time()
        results = self.model(self.image_path)
        cost = time.time() - start

        det = results.xyxy[0]

        count = {"recyclable_waste":0,"kitchen_waste":0,"hazardous_waste":0,"other_waste":0}

        text = ""

        for d in det:
            cls = int(d[5])
            name = self.names[cls]
            cn = self.cls_map.get(name, name)

            text += cn + "\n"

            if name in count:
                count[name] += 1

        self.label_stats(cost, len(det), count)

        img = results.render()[0]

        save_path = os.path.join(self.result_dir, f"img_{int(time.time())}.jpg")
        cv2.imwrite(save_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

        self.show_img(save_path, self.label_right)

        self.result_text.setText(text)

        self.history.append([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            os.path.basename(self.image_path),
            len(det),
            count["recyclable_waste"],
            count["kitchen_waste"],
            count["hazardous_waste"],
            count["other_waste"]
        ])

        self.history = self.history[-20:]

    # ---------------- CAMERA ----------------
    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()

    def update_camera(self):

        ret, frame = self.cap.read()
        if not ret:
            return

        results = self.model(frame)
        frame = results.render()[0]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = rgb.shape
        q = QImage(rgb.data, w, h, c*w, QImage.Format_RGB888)

        self.label_right.setPixmap(QPixmap.fromImage(q).scaled(self.label_right.size(), Qt.KeepAspectRatio))

    # ---------------- EXCEL ----------------
    def export_excel(self):

        file_path = os.path.join(self.result_dir, f"report_{int(time.time())}.xlsx")

        wb = Workbook()
        ws = wb.active
        ws.append(["时间","图片","目标","可回收","厨余","有害","其他"])

        for r in self.history:
            ws.append(r)

        wb.save(file_path)

    # ---------------- CLEAR ----------------
    def clear_all(self):
        self.result_text.clear()

    # ---------------- STATS ----------------
    def label_stats(self, cost, total, count):
        self.time_label.setText(str(round(cost,3)))
        self.total_label.setText(str(total))
        self.rec_label.setText(str(count["recyclable_waste"]))
        self.kit_label.setText(str(count["kitchen_waste"]))
        self.haz_label.setText(str(count["hazardous_waste"]))
        self.oth_label.setText(str(count["other_waste"]))


# =========================
# 启动函数（带loading）
# =========================
def run():

    app = QApplication(sys.argv)

    loading = LoadingWindow()
    loading.show()

    app.processEvents()  # ⭐关键：强制刷新UI

    win = GarbageGUI()

    # ⭐关键：先让loading显示，再加载模型
    win.load_model()

    loading.close()
    win.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    run()