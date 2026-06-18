import sys
import os
import cv2
import torch

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit
)

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer


class GarbageDetector(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("智能垃圾分类识别系统")
        self.resize(1200, 700)

        self.image_path = None
        self.cap = None

        self.timer = QTimer()

        self.timer.timeout.connect(self.update_camera)

        print("开始加载模型...")

        weight_path = os.path.join(
            os.path.dirname(__file__),
            "weights",
            "garbage_v1_best.pt"
        )

        self.model = torch.hub.load(
            '..',
            'custom',
            path=weight_path,
            source='local'
        )

        print("模型加载成功")

        self.init_ui()

    
    def init_ui(self):

        self.btn_select = QPushButton("📁 选择图片")
        self.btn_detect = QPushButton("🔍 开始检测")

        self.btn_camera = QPushButton("📷 打开摄像头")
        self.btn_stop = QPushButton("⛔ 关闭摄像头")

        self.btn_select.clicked.connect(self.select_image)
        self.btn_detect.clicked.connect(self.detect_image)

        self.btn_camera.clicked.connect(self.start_camera)
        self.btn_stop.clicked.connect(self.stop_camera)

        self.label_original = QLabel("原图预览")
        self.label_result = QLabel("检测结果")

        self.label_original.setFixedSize(560, 420)
        self.label_result.setFixedSize(560, 420)

        self.label_original.setAlignment(Qt.AlignCenter)
        self.label_result.setAlignment(Qt.AlignCenter)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFixedHeight(180)

        title = QLabel("♻ 智能垃圾分类识别系统")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
            color:#2C3E50;
            border:none;
            background:none;
            padding:10px;
        """)

        image_layout = QHBoxLayout()
        image_layout.addWidget(self.label_original)
        image_layout.addWidget(self.label_result)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_select)
        button_layout.addWidget(self.btn_detect)
        button_layout.addWidget(self.btn_camera)
        button_layout.addWidget(self.btn_stop)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(image_layout)
        main_layout.addWidget(self.result_text)

        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget{
                background-color:#F5F7FA;
                font-size:14px;
                font-family:Microsoft YaHei;
            }

            QPushButton{
                background-color:#409EFF;
                color:white;
                border:none;
                border-radius:10px;
                padding:10px;
                font-weight:bold;
            }

            QPushButton:hover{
                background-color:#66B1FF;
            }

            QPushButton:pressed{
                background-color:#337ECC;
            }

            QLabel{
                background:white;
                border:2px solid #DCDFE6;
                border-radius:12px;
            }

            QTextEdit{
                background:white;
                border:2px solid #DCDFE6;
                border-radius:12px;
                padding:8px;
                font-size:14px;
            }
        """)

    def select_image(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            "Images (*.jpg *.jpeg *.png)"
        )

        if file_path:
            self.image_path = file_path
            self.show_image(file_path, self.label_original)

    def show_image(self, image_path, label):

        img = cv2.imread(image_path)

        if img is None:
            return

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        h, w, ch = img.shape
        bytes_per_line = ch * w

        qt_img = QImage(
            img.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_RGB888
        )

        pixmap = QPixmap.fromImage(qt_img)

        label.setPixmap(
            pixmap.scaled(
                label.width(),
                label.height(),
                Qt.KeepAspectRatio
            )
        )

    def detect_image(self):

        if not self.image_path:
            return

        results = self.model(self.image_path)

        img = results.render()[0]

        img = cv2.cvtColor(
            img,
            cv2.COLOR_RGB2BGR
        )

        save_dir = os.path.join(
            os.path.dirname(__file__),
            "result"
        )

        os.makedirs(
            save_dir,
            exist_ok=True
        )

        file_name = os.path.basename(
            self.image_path
        )

        result_path = os.path.join(
            save_dir,
            file_name
        )

        cv2.imwrite(
            result_path,
            img
        )

        self.show_image(
            result_path,
            self.label_result
        )

        names = self.model.names

        cn_names = {
            "recyclable_waste": "可回收垃圾",
            "kitchen_waste": "厨余垃圾",
            "hazardous_waste": "有害垃圾",
            "other_waste": "其他垃圾"
        }

        counts = {
            "recyclable_waste": 0,
            "kitchen_waste": 0,
            "hazardous_waste": 0,
            "other_waste": 0
        }

        detections = results.xyxy[0]

        text = "检测结果\n\n"

        for det in detections:

            cls_id = int(det[5])
            conf = float(det[4])

            cls_name = names[cls_id]

            text += f"{cn_names.get(cls_name, cls_name)}  置信度:{conf:.2f}\n"

            if cls_name in counts:
                counts[cls_name] += 1

        text += "\n垃圾统计\n\n"

        text += f"可回收垃圾：{counts['recyclable_waste']}\n"
        text += f"厨余垃圾：{counts['kitchen_waste']}\n"
        text += f"有害垃圾：{counts['hazardous_waste']}\n"
        text += f"其他垃圾：{counts['other_waste']}\n"

        text += "\n投放建议\n\n"

        if counts["recyclable_waste"] > 0:
            text += "请投入可回收垃圾桶\n"

        if counts["kitchen_waste"] > 0:
            text += "请投入厨余垃圾桶\n"

        if counts["hazardous_waste"] > 0:
            text += "请投入有害垃圾桶\n"

        if counts["other_waste"] > 0:
            text += "请投入其他垃圾桶\n"

        self.result_text.setText(text)

    def start_camera(self):

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.result_text.setText("摄像头打开失败")
            return

        self.timer.start(30)

        self.result_text.setText("摄像头已开启")


    def stop_camera(self):

        self.timer.stop()

        if self.cap:
            self.cap.release()

        self.label_original.clear()
        self.label_result.clear()

        self.result_text.setText("摄像头已关闭")


    def update_camera(self):

        if self.cap is None:
            return

        ret, frame = self.cap.read()

        if not ret:
            return

        results = self.model(frame)

        result_img = results.render()[0]

        # 原图
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        h, w, ch = rgb_frame.shape

        qt_img = QImage(
            rgb_frame.data,
            w,
            h,
            ch * w,
            QImage.Format_RGB888
        )

        self.label_original.setPixmap(
            QPixmap.fromImage(qt_img).scaled(
                self.label_original.width(),
                self.label_original.height(),
                Qt.KeepAspectRatio
            )
        )

        # 检测结果
        h, w, ch = result_img.shape

        qt_result = QImage(
            result_img.data,
            w,
            h,
            ch * w,
            QImage.Format_RGB888
        )

        self.label_result.setPixmap(
            QPixmap.fromImage(qt_result).scaled(
                self.label_result.width(),
                self.label_result.height(),
                Qt.KeepAspectRatio
            )
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = GarbageDetector()

    window.show()

    sys.exit(app.exec_())