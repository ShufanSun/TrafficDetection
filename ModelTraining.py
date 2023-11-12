from ultralytics import YOLO
import os
import cv2
import numpy as np
import docopt
import glob
from IPython.display import HTML
from IPython.core.display import Video
from moviepy.editor import VideoFileClip
from cam_calib import camera_calibrate
lanes = cv2.imread('./Images/lane.png')
gray = cv2.cvtColor(lanes, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
kernel = np.ones((1, 1), np.uint8)  # Adjust the size of the kernel for erosion

eroded_edges = cv2.erode(edges, kernel, iterations=1)
minLineLength = 100  # Adjust this minimum line length as needed
maxLineGap = 10      # Adjust maximum gap between lines as needed

lines = cv2.HoughLinesP(eroded_edges, 1, np.pi / 90, threshold=100, minLineLength=minLineLength, maxLineGap=maxLineGap)
lanes_with_lines = lanes.copy()
height, width = lanes.shape[:2]
half_height = height // 2  # Calculate the midpoint of the image height
half_width = width // 2
right_lines = []
left_lines = []

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if y1 >= half_height and y2 >= half_height:
            if x1 > half_width and x2 > half_width:
                right_lines.append(line)
            elif x1 < half_width and x2 < half_width:
                left_lines.append(line)

if right_lines and left_lines:
    # Calculate the bisector line between left and right lines
    right_line = max(right_lines, key=lambda line: max(line[0][1], line[0][3]))
    left_line = max(left_lines, key=lambda line: max(line[0][1], line[0][3]))

    right_slope = (right_line[0][3] - right_line[0][1]) / (right_line[0][2] - right_line[0][0]) if (right_line[0][2] - right_line[0][0]) != 0 else 1e6
    left_slope = (left_line[0][3] - left_line[0][1]) / (left_line[0][2] - left_line[0][0]) if (left_line[0][2] - left_line[0][0]) != 0 else 1e6

    bisector_slope = (right_slope + left_slope) / 2
    bisector_intercept = (half_height - right_slope * half_width + half_height - left_slope * half_width) / 2

    # Filter lines based on proximity to bisector and similar absolute slopes
    selected_lines = []
    for line in right_lines + left_lines:
        slope = (line[0][3] - line[0][1]) / (line[0][2] - line[0][0]) if (line[0][2] - line[0][0]) != 0 else 1e6
        intercept = line[0][1] - slope * line[0][0]
        intersection_x = int((half_height - intercept) / slope) if slope != 0 else line[0][0]

        if (abs(slope) > 0.1 and abs(slope) < 3) and abs(abs(slope) - abs(bisector_slope)) > 0.5 * abs(bisector_slope) and abs(intersection_x - (width // 2)) < 0.1 * width:

            selected_lines.append(line)
    
    if len(selected_lines) >= 2:
        # Choose the line with the smallest x value on each side
        left_line = min([line for line in selected_lines if line[0][2] < half_width], key=lambda l: l[0][0])
        right_line = min([line for line in selected_lines if line[0][2] > half_width], key=lambda l: l[0][0])

        left_slope = (left_line[0][3] - left_line[0][1]) / (left_line[0][2] - left_line[0][0]) if (left_line[0][2] - left_line[0][0]) != 0 else 1e6
        right_slope = (right_line[0][3] - right_line[0][1]) / (right_line[0][2] - right_line[0][0]) if (right_line[0][2] - right_line[0][0]) != 0 else 1e6

        left_intercept = left_line[0][1] - left_slope * left_line[0][0]
        right_intercept = right_line[0][1] - right_slope * right_line[0][0]

        left_intersection_x = int((half_height - left_intercept) / left_slope) if left_slope != 0 else left_line[0][0]
        right_intersection_x = int((half_height - right_intercept) / right_slope) if right_slope != 0 else right_line[0][0]

        cv2.line(lanes_with_lines, (left_line[0][0], left_line[0][1]), (left_intersection_x, half_height), (0, 0, 255), 2)
        cv2.line(lanes_with_lines, (right_line[0][0], right_line[0][1]), (right_intersection_x, half_height), (0, 0, 255), 2)

# Lines extension to the bottom of the frame
left_extension_x = int(left_line[0][2] - left_slope * (left_line[0][3] - height))
right_extension_x = int(right_line[0][2] - right_slope * (right_line[0][3] - height))

# Drawing extended lines
cv2.line(lanes_with_lines, (left_line[0][2], left_line[0][3]), (left_extension_x, height), (0, 0, 255), 2)
cv2.line(lanes_with_lines, (right_line[0][2], right_line[0][3]), (right_extension_x, height), (0, 0, 255), 2)

# Intersection of extended lines
intersection_x = int((height - left_intercept) / left_slope)
cv2.circle(lanes_with_lines, (intersection_x, height), 5, (255, 0, 0), -1)

# Height of trapezoid
height_of_trapezoid = height - intersection_x

# Calculate the center point for the top of the trapezoid
center_top_x = (left_intersection_x + right_intersection_x) // 2
center_top_y = half_height

# Divide the height in half
half_height_of_trapezoid = height_of_trapezoid // 2

# Draw the trapezoid
# pts = np.array([[left_intersection_x, half_height], [right_intersection_x, half_height], [right_extension_x, height], [left_extension_x, height]], np.int32)
# cv2.fillPoly(lanes_with_lines, [pts], (0, 255, 0))
top_left_x = (left_extension_x + right_intersection_x)
top_right_x = (right_extension_x + left_intersection_x)//2

# Draw the trapezoid
pts = np.array([
   [top_left_x,center_top_y],
    [left_line[0][2], left_line[0][3]],
    [right_line[0][2], right_line[0][3]],
    [right_line[0][0], right_line[0][1]]
], np.int32)
alpha = 0.4  # Alpha value for transparency (0 = transparent, 1 = opaque)
color = (0, 255, 0, int(255 * alpha))  # The color (0, 255, 0) with alpha transparency

pts = np.array([
   [top_left_x, center_top_y],
   [left_line[0][2], left_line[0][3]],
   [right_line[0][2], right_line[0][3]],
   [right_line[0][0], right_line[0][1]]
], np.int32)

overlay = lanes.copy()
cv2.fillPoly(overlay, [pts], color)

output = cv2.addWeighted(overlay, alpha, lanes, 1 - alpha, 0)

cv2.imshow('Selected Lines with Trapezoid', output)
cv2.waitKey(0)
cv2.destroyAllWindows()