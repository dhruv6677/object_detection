#  Sign Language Detection using YOLOv5

A real-time **Sign Language Detection** project built using **YOLOv5** and Python. The system detects sign language gestures from images or video streams and is organized with a modular pipeline architecture for easy maintenance and future expansion.

---

#  Overview

This project leverages the **YOLOv5 (You Only Look Once v5)** object detection model to recognize sign language gestures. It can be adapted for applications such as accessibility tools, educational platforms, and human-computer interaction.

---

#  Features

- 🔍 Real-time sign language detection
- 🎯 Powered by YOLOv5 for fast and accurate inference
- 📂 Modular project structure
- ⚙️ Configuration-driven workflow
- 📊 Artifact management for models and outputs
- 🖥️ Easy to extend for training and deployment
- 🐍 Built with Python 3.10

---


#  Tech Stack

- Python 3.10
- YOLOv5
- PyTorch
- OpenCV
- NumPy
- Pandas
- Conda

---

#  Installation

## 1. Clone the repository

```bash
git clone https://github.com/dhruv6677/object_detection.git
cd object_detection
```

## 2. Create a Conda environment

```bash
conda create -n signlang python=3.10 -y
```

## 3. Activate the environment

```bash
conda activate signlang
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

#  Run the Project

Start the application with:

```bash
python app.py
```

---

#  Workflow

```text
                +----------------+
                |    app.py      |
                +-------+--------+
                        |
                        v
               +------------------+
               |    Pipeline      |
               +--------+---------+
                        |
        +---------------+----------------+
        |                                |
        v                                v
+------------------+            +------------------+
| Config Entities  |            |    Constants     |
+------------------+            +------------------+
        |
        v
+------------------+
| YOLOv5 Components |
+------------------+
        |
        v
+------------------+
| Detection Output |
+------------------+
        |
        v
+------------------+
| Saved Artifacts  |
+------------------+
```

---

#  Dataset

Train the model using a labeled sign language dataset in YOLO format:

```
dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
├── labels/
│   ├── train/
│   ├── val/
│   └── test/
└── data.yaml
```

---

# Example Use Cases

- American Sign Language (ASL) alphabet detection
- Educational learning tools
- Accessibility applications
- Gesture-based user interfaces
- Real-time webcam recognition systems

---

#  Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

---





# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

A YOLOv5-based Sign Language Detection project designed with a modular architecture for scalable development and real-time gesture recognition.