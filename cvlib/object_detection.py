import cv2
import numpy as np
import os
from ultralytics import YOLO

class ObjectDetection:
    def __init__(self, model_path="./YOLOV8N-Vehicle/train/weights/best.pt", conf = 0.2, iou = 0.7, device = None):
        print("Dectector model is loading...")
        self.model = YOLO(model_path)
        self.conf = conf
        self.iou = iou
        self.device = device
        print("Dectector model is ready now")
    def predict(self, frame):
        results = self.model.predict(frame, conf=self.conf, iou=self.iou, device=self.device)
        results[0] = results[0].numpy()
        return results[0].boxes.xyxy

