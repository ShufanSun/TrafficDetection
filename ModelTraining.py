from ultralytics import YOLO
import os
import cv2
import numpy as np
import docopt
from IPython.display import HTML
from IPython.core.display import Video
from moviepy.editor import VideoFileClip
from cam_calib import camera_calibrate
lanes = cv2.imread('./Images/lane.png')
gray = cv2.cvtColor(lanes, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
kernel = np.ones((1, 1), np.uint8)  # Adjust the size of the kernel for erosion

eroded_edges = cv2.erode(edges, kernel, iterations=1)
lines = cv2.HoughLines(eroded_edges, 1, np.pi / 180, threshold=100)  # Adjust threshold as needed

# Display the eroded edges
cv2.imshow('Eroded Edges', eroded_edges)
cv2.waitKey(0)  # Wait for any key press
cv2.destroyAllWindows()
