from ultralytics import YOLO
import cv2
from PIL import Image
import os
from time import sleep

model = YOLO("yolov8-trained_openvino_model/", "segment")

video_path = './Videos/out4.mp4'
cap = cv2.VideoCapture(video_path)

i = 0

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        i += 1
        if i % 5 != 0:
            # remove sleep for maxumum speed
            sleep(1/20)
            continue

        results = model(frame)
       
        for result in results:
            boxes = result.boxes  # Boxes object for bbox outputs
            masks = result.masks  # Masks object for segmentation masks outputs
            keypoints = result.keypoints  # Keypoints object for pose outputs
            probs = result.probs  # Probs object for classification outputs
    
        for idx, r in enumerate(results):
            im_array = r.plot()  # plot a BGR numpy array of predictions

        small = cv2.resize(im_array, (0,0), fx=0.5, fy=0.5)

        cv2.imshow("Traffic Detection", small)
        cv2.waitKey(1)
            
    else:
        cap.release()
        break