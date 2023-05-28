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
    def predict(self, frame, specific_class = None, threshold = 30):
        """_summary_
        predict the frame and return the result
        Args:
            frame (_type_): frame to predict numpy array
            specific_class (list optional): List of class you want to extract. Defaults to None. Mean that you want to extract all class.

        Returns:
            list: list of result object with class, confidence, and bounding box
        """
        results = self.model.predict(frame, conf=self.conf, iou=self.iou, device=self.device, verbose=False)
        b_results = results[0].numpy().boxes
        clses = b_results.cls.astype(int)
        xxyys = b_results.xyxy.astype(int)
        if specific_class is not None:
            clses = clses[np.isin(clses, specific_class)]
            xxyys = np.array([xxyys[i] for i in range(len(clses)) if (clses[i] in specific_class) and (xxyys[i][2] - xxyys[i][0] > threshold)])
        return xxyys, clses

