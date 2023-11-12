from ultralytics import YOLO
import cv2
import os
from glob import glob

# Load the YOLO model
model = YOLO("yolov8-trained.pt")  # Provide the path to your pre-trained YOLO model

# Load the video
video_path = './Videos/out4.mp4'
video = glob('*.mp4')
cap = cv2.VideoCapture(video_path)
i = 0

# Loop through the video frames
while cap.isOpened():
	ret, frame = cap.read()
	if ret:
		cv2.imwrite('frame{:d}.jpg'.format(i), frame)
		i += 20
		cap.set(cv2.CAP_PROP_POS_FRAMES, i)
		print(i)
	else:
		cap.release()
		break

	# i+=1
	# if i != 5:
	#     cap.release
	# # # Read a frame from the video
	# success, frame = cap.read()
	# while True:
	#     cap.set(cv2.CAP_PROP_FPS,2) 
	#     ret,frame = cap.read()
	#     i=i+1
	#     print(cap.get(cv2.CAP_PROP_FPS))
	#     print(i)

	# if success:
	#     # Run YOLOv8 inference on the frame
	#     results = model(frame)

	#     # Visualize the results on the frame
	#     annotated_frame = results[0].plot()

	#     # Display the annotated frame
	#     cv2.imshow("YOLOv8 Inference", annotated_frame)
