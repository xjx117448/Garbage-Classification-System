# 基于YOLOv5的智能垃圾分类识别系统

## 项目简介

本项目基于YOLOv5目标检测算法实现智能垃圾分类识别系统，可对垃圾进行实时检测与分类，并提供图形化操作界面。

## 功能介绍

* 图片垃圾识别
* 摄像头实时检测
* 四分类垃圾识别
* 检测结果可视化
* 垃圾数量统计
* PyQt5图形界面

## 垃圾类别

| 类别编号 | 类别名称  |
| ---- | ----- |
| 0    | 可回收垃圾 |
| 1    | 厨余垃圾  |
| 2    | 有害垃圾  |
| 3    | 其他垃圾  |

## 技术栈

* Python
* PyTorch
* YOLOv5
* OpenCV
* PyQt5

## 模型性能

* 数据集规模：约1700张图像
* 类别数量：4类
* mAP50：83.7%
* GPU：RTX 4080 Laptop

## 项目结构

garbage_system/

├── garbage_gui.py

├── weights/

│   └── garbage_v1_best.pt

├── result/

├── images/

├── README.md

└── requirements.txt

## 运行方式

安装依赖：

pip install -r requirements.txt

启动程序：

python garbage_gui.py
