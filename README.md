♻ 基于 YOLOv5 的智能垃圾分类识别系统（GUI可视化）
📌 项目简介

本项目基于 YOLOv5目标检测算法 与 PyQt5图形界面开发技术，实现了一个智能垃圾分类识别系统。系统支持图片检测与摄像头实时检测，并对检测结果进行可视化展示与统计分析，可用于智能垃圾分类场景的原型验证与教学展示。

🎯 功能介绍
📷 图片垃圾检测识别
🎥 摄像头实时检测
🧠 基于YOLOv5的目标检测模型
📊 垃圾类别统计与数量分析
⏱ 检测耗时显示
🖥 PyQt5图形化交互界面
♻ 自动垃圾分类提示
🗂 垃圾类别定义
类别编号	类别名称
0	可回收垃圾
1	厨余垃圾
2	有害垃圾
3	其他垃圾
🧠 技术栈
Python 3.x
PyTorch
YOLOv5
OpenCV
PyQt5
📁 项目结构
Garbage-Classification-System
│
├── garbage_gui_pro.py        # GUI主程序
├── detect.py                 # YOLOv5检测脚本
├── requirements.txt          # 依赖环境
├── README.md
│
├── weights/
│   └── garbage_v1_best.pt    # 模型文件（本地使用）
│
├── screenshots/              # 项目截图
│   ├── gui_main.png
│   ├── detect_result.png
│   └── camera_mode.png
🚀 运行方式
1️⃣ 安装依赖
pip install -r requirements.txt
2️⃣ 下载YOLOv5环境（如未配置）
git clone https://github.com/ultralytics/yolov5
3️⃣ 运行GUI界面
python garbage_gui_pro.py
📊 模型说明

本项目采用 YOLOv5 进行训练，数据集包含约：

📦 1700+ 张垃圾图像
♻ 4 类垃圾类别

模型性能：

mAP@0.5 ≈ 83.7%
支持实时推理（CPU / GPU）
🖥 界面展示
🧾 主界面

（在这里放截图）

screenshots/gui_main.png
🔍 检测效果

（在这里放检测结果截图）

screenshots/detect_result.png
📷 摄像头模式

（在这里放实时检测截图）

screenshots/camera_mode.png
📈 项目特点

✔ 集成目标检测 + GUI系统
✔ 支持实时视频流检测
✔ 可视化检测结果
✔ 自动统计垃圾类别数量
✔ 工程化结构设计（非单脚本实验）

📌 未来优化方向
增加检测历史记录功能
导出 Excel 检测报告
优化轻量化模型（部署端侧）
增加 Web 端展示版本
支持多模型切换（YOLOv5 / YOLOv8）
👨‍💻 作者信息
GitHub: https://github.com/xjx117448
Project: Garbage Classification System
⭐ 如果有帮助

如果该项目对你有帮助，可以点一个 ⭐ Star 支持一下。
