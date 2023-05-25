import cv2
import numpy as np
from cvlib.object_detection import ObjectDetection
from cvlib.tracker import EuclideanDistTracker
from ultralytics import YOLO
import time
video_capture = cv2.VideoCapture("./Videos/camera3.mp4")



width = 848
height = 477
dim = (width, height)
def image_resize(img, dim):
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

def image_preprocess(img):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    equal = cv2.equalizeHist(blur)
    return equal

fps = video_capture.get(cv2.CAP_PROP_FPS)
real_time = round(1000/fps)
target_fps = 20

detector = ObjectDetection(iou=0.5)
tracker = EuclideanDistTracker()
base_dis = 25

counter = 0
targer_counter = 1;
cap_x, cap_y, cap_w, cap_h = 200, 270, 420, 200 
line = cap_h//2
show_cap = True

dis_scalar = (targer_counter+1)/targer_counter
acceptable = 5
while True:

    if counter == targer_counter:
        counter = 0;
        ret = video_capture.grab()
        continue
    counter += 1

    ret, frame = video_capture.read()
    if ret:

        frame = image_resize(frame, dim)
        roi = frame[cap_y:cap_y + cap_h, cap_x:cap_x + cap_w]
        results = detector.predict(roi)
        if show_cap:
            cv2.rectangle(frame, (cap_x, cap_y), (cap_x + cap_w, cap_y + cap_h), (255, 255, 0), 2)
            cv2.line(roi, (0, line), (cap_w, line), (107, 214, 205), 2)
            cv2.line(roi, (0, line+acceptable), (cap_w, line+acceptable), (214, 214, 214), 2)
            cv2.line(roi, (0, line-acceptable), (cap_w, line-acceptable), (214, 214, 214), 2)
        
        if len(results) > 0:
            presults = tracker.update( results.astype(int), liney = line, acceptable = acceptable, delta = base_dis*dis_scalar)
            for package in presults:
                ux, uy, lx, ly, id, direction = package 
                cv2.rectangle(roi, (ux, uy), (lx, ly), (0, 255, 0), 2)
                cv2.putText(roi, f"id: {str(id)}|{'in' if direction==1 else 'out'}", ((ux+lx)//2, uy + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, f"Vehicle Count: {str(tracker.count)}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        

        cv2.imshow("frame", frame)
    else:
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    waiting_time = int(1000/fps)
    key = cv2.waitKey(1)
    if key == ord('x'):
        break




video_capture.release()
cv2.destroyAllWindows()

