🗑️ Garbage Classification System (YOLOv5-based)
📌 Overview

This project is a deep learning-based garbage classification system built on top of YOLOv5.
It can detect and classify different types of waste in images in real time through a GUI interface.

The system is designed for:

Intelligent waste sorting scenarios
Educational computer vision projects
YOLOv5 practical deployment practice
🚀 Features
🎯 Real-time garbage detection using YOLOv5
🧠 Supports custom-trained dataset (4-class / multi-class expandable)
🖥️ PyQt5-based graphical user interface (GUI)
📷 Image-based detection (supports upload & preview)
📊 Detection results visualization (bounding boxes + labels)
💾 Optional result logging / saving support
🧠 Model Architecture
Backbone: YOLOv5 (Ultralytics)
Input size: 640×640
Framework: PyTorch
Training type: Custom dataset fine-tuning

Supported classes (example):

Recyclable waste
Hazardous waste
Kitchen waste
Other waste
🖼️ Demo

Replace images with your actual screenshots in /screenshots

🧩 GUI Interface

🔍 Detection Result

🏗️ Project Structure
garbage_system/
│
├── garbage_gui.py              # Main GUI interface
├── garbage_gui_final.py        # Optimized GUI version
├── garbage_gui_pro.py          # Pro version UI
├── detect.py                   # YOLOv5 inference script
├── best.pt                     # Trained model weights
│
├── runs/                       # Detection outputs
├── datasets/                   # Training dataset
├── utils/                      # YOLO utilities
│
├── screenshots/                # Project demo images
│   ├── gui.png
│   ├── result.png
│
└── README.md
⚙️ Installation
1. Clone repository
git clone https://github.com/xjx117448/Garbage-Classification-System.git
cd Garbage-Classification-System
2. Install dependencies
pip install -r requirements.txt

If YOLOv5 dependencies are missing:

pip install torch torchvision opencv-python pyqt5 openpyxl
▶️ Usage
Run GUI system
python garbage_gui_final.py
Run detection (CLI mode)
python detect.py --weights best.pt --source your_image.jpg
🧪 Workflow
Load image via GUI
YOLOv5 performs inference
Bounding boxes are generated
Results displayed in interface
Optional: save output image
📊 Performance
Metric	Value
Model	YOLOv5
Input size	640
Classes	4 (expandable)
Framework	PyTorch
🔧 Possible Improvements
Add video stream detection (webcam / RTSP)
Deploy as web system (Flask / FastAPI)
Optimize model for edge devices (TensorRT / ONNX)
Add database logging for detection history
Improve dataset diversity
📌 Notes
This project is intended for learning and research purposes
Model performance depends on dataset quality
GUI built using PyQt5 for desktop deployment
👤 Author
GitHub: xjx117448
⭐ Acknowledgements
YOLOv5 by Ultralytics
Open-source computer vision community
