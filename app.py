import sys
import os
import cv2
import torch
import numpy as np
import pathlib
from flask import Flask, request, jsonify, render_template, Response
from signLanguage.exception import SignException
from signLanguage.utils.main_utils import decodeImage, encodeImageIntoBase64

app = Flask(__name__)

# Load YOLOv5 model
MODEL_PATH = "models/best.pt"
pathlib.PosixPath = pathlib.WindowsPath  # fix Linux->Windows path issue

model = torch.hub.load('yolov5', 'custom', path=MODEL_PATH, source='local')
model.conf = 0.25  # confidence threshold

# ─────────────────────────────────────────────
# HOME ROUTE
# ─────────────────────────────────────────────


@app.route("/")
def home():
    return render_template("index.html")


# ─────────────────────────────────────────────
# IMAGE PREDICTION ROUTE
# ─────────────────────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Decode base64 image from request
        image_data = request.json.get("image")
        decodeImage(image_data, "input.jpg")

        # Run prediction
        img = cv2.imread("input.jpg")
        results = model(img)

        # Draw boxes on image
        result_img = results.render()[0]
        cv2.imwrite("output.jpg", result_img)

        # Get detected class names
        labels = results.pandas().xyxy[0]["name"].tolist()
        confidences = results.pandas().xyxy[0]["confidence"].tolist()

        detections = [
            {"label": label, "confidence": round(float(conf), 2)}
            for label, conf in zip(labels, confidences)
        ]

        # Encode result image to base64
        encoded_image = encodeImageIntoBase64("output.jpg")

        return jsonify({
            "status": "success",
            "detections": detections,
            # "image": encoded_image.decode("utf-8")
            "image": str(encoded_image)
        })

    except Exception as e:
        raise SignException(e, sys)


# ─────────────────────────────────────────────
# LIVE WEBCAM ROUTE
# ─────────────────────────────────────────────
def generate_frames():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        # Print what model sees
        df = results.pandas().xyxy[0]
        if len(df) > 0:
            print(df[["name", "confidence"]])  # ← shows detections in terminal
        else:
            print("Nothing detected...")      # ← shows if model sees nothing

        frame = results.render()[0]
        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )

    cap.release()
    
@app.route("/live")
def live():
    return render_template("live.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ─────────────────────────────────────────────
# TRAIN ROUTE (optional)
# ─────────────────────────────────────────────
@app.route("/train")
def train():
    try:
        from signLanguage.pipeline.training_pipeline import TrainPipeline
        obj = TrainPipeline()
        obj.run_pipeline()
        return jsonify({"status": "success", "message": "Training complete!"})
    except Exception as e:
        raise SignException(e, sys)


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
