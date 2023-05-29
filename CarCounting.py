import cv2
import numpy as np
from cvlib.object_detection import ObjectDetection
from cvlib.tracker import EuclideanDistTracker
from ultralytics import YOLO
import time
video_name = 'camera2'
video_capture = cv2.VideoCapture(f"./Videos/{video_name}.mp4")
# Name for class
class_ref =['car', 'motorbike']
# Class to take set None to take all class
take_class = [0]
# Is render the video
render = True
# Video resize
width = 848
height = 477
dim = (width, height)
def image_resize(img, dim):
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


fps = video_capture.get(cv2.CAP_PROP_FPS)

detector = ObjectDetection(conf = 0.35,iou=0.5)
tracker = EuclideanDistTracker()
# Distance between two point to be consider as same object
base_dis = 25
# Skip frame-th to reduce the number of frame to process
targer_counter = 1;
counter = 0;
# Cut the frame to reduce the number of frame to process
frameCut = False;
# cut the frame to this size to reduce time to process
# cap_x, cap_y, cap_w, cap_h = 200, 270, 420, 200 
cap_x, cap_y, cap_w, cap_h = 0, 0, width, height 
line = int(cap_h*0.70)
show_cap = True
# Distance scalar to increase the distance between two point to be consider as same object in case of high speed and low fps
dis_scalar = (targer_counter+1)/targer_counter
# Acceptable distance from line
acceptable = 10
# Video output in case of render is True
video_results = cv2.VideoWriter(f'Videos_ouput/{video_name}_result.avi',cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width,height))

def draw_with_alpha(img, draw_function, up, lp, color, width, alpha=0.5):
    overlay = np.zeros_like(img, dtype=np.uint8)
    draw_function(overlay, up, lp, color, width)
    mask = overlay.astype(bool)
    img[mask] = cv2.addWeighted(img, alpha, overlay, 1 - alpha, 0)[mask]


while True:
    if frameCut:
        if counter == targer_counter:
            counter = 0;
            ret = video_capture.grab()
            continue
        counter += 1

    ret, frame = video_capture.read()
    if ret:

        frame = image_resize(frame, dim)
        roi = frame[cap_y:cap_y + cap_h, cap_x:cap_x + cap_w]
        results, classes = detector.predict(roi, specific_class=take_class)
        if show_cap:
            #cv2.rectangle(frame, (cap_x, cap_y), (cap_x + cap_w, cap_y + cap_h), (255, 255, 0), 2)
            cv2.line(roi, (0, line), (cap_w, line), (107, 214, 205), 2)
            draw_with_alpha(frame, cv2.rectangle, (cap_x, cap_y), (cap_x + cap_w, cap_y + cap_h), (255, 255, 0), 2)
            # cv2.line(roi, (0, line+acceptable), (cap_w, line+acceptable), (214, 214, 214), 2)
            # cv2.line(roi, (0, line-acceptable), (cap_w, line-acceptable), (214, 214, 214), 2)
            draw_with_alpha(roi, cv2.line, (0, line+acceptable), (cap_w, line+acceptable), (214, 214, 214), 2)
            draw_with_alpha(roi, cv2.line, (0, line-acceptable-10), (cap_w, line-acceptable-10), (214, 214, 214), 2, 0.8)
        
        if len(results) > 0:
            presults = tracker.update( results, liney = line, acceptable = acceptable, delta = base_dis*dis_scalar)
            for i, package in enumerate(presults):
                ux, uy, lx, ly, id, direction = package 
                cv2.rectangle(roi, (ux, uy), (lx, ly), (0, 220, 0), 2)
                cv2.putText(roi, f"id: {str(id)}|{'in' if direction==1 else 'out'} class: {class_ref[classes[i]]}", (ux, uy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, f"Vehicle Count: {str(tracker.count)}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        if render:
            video_results.write(frame)
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

