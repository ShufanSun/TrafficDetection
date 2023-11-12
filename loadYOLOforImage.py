from ultralytics import YOLO
from PIL import Image
import cv2
from LaneDetection import LaneDetector
model = YOLO("yolov8-trained.pt")

results = model(['./Images/lane2.jpg', './Images/lane3.jpg'], stream=True)  # return a generator of Results objects

# Process results generator
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    
results = model(['./Images/lane2.jpg', './Images/lane3.jpg'])  # list of 2 Results objects
for r in results:
    print(r.boxes)  # print the Boxes object containing the detection bounding boxes
    
# Show the results
for r in results:
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.show()  # show image
    
# from ultralytics import YOLO
# from PIL import Image
# import cv2
# from LaneDetection import LaneDetector

# class LaneDetectionWithYOLO:
#     def __init__(self, model_path="yolov8-trained.pt"):
#         self.model = YOLO(model_path)
    
#     def detect_and_visualize_lanes(self, image_path):
#         # Assuming detect_and_visualize_lanes is the function you've created
#         LaneDetector.detect_lanes(image_path)

#     def process_images(self, image_paths):
#         results = self.model(image_paths, stream=True)  # return a generator of Results objects

#         # Process results generator
#         for result in results:
#             boxes = result.boxes  # Boxes object for bbox outputs
#             masks = result.masks  # Masks object for segmentation masks outputs
#             keypoints = result.keypoints  # Keypoints object for pose outputs
#             probs = result.probs  # Probs object for classification outputs

#         results = self.model(image_paths)  # list of Results objects
#         for r in results:
#             print(r.boxes)  # print the Boxes object containing the detection bounding boxes

#         # Show the results
#         for r in results:
#             im_array = r.plot()  # plot a BGR numpy array of predictions
#             im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
#             im.show()

# # Example usage
# # lane_detection = LaneDetector.detect_and_visualize_lanes('./Images/lane2.jpg')
# lane_detection = LaneDetectionWithYOLO('./Images/lane2.jpg')

