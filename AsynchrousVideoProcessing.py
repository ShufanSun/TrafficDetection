from ultralytics import YOLO
import cv2
import numpy as np
import torch
import time
class Async:
    def __init__(self):
        self.model = YOLO("yolov8-trained.pt")
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("\n\nDevice Used:", self.device)

    def score_frame(self, frame):
        results = self.model(frame)
        annotated_frame = self.annotate_frame(frame, results)
        return annotated_frame

    def annotate_frame(self, frame, results):
        annotated_frame = frame.copy()  # Create a copy of the frame
        for result in results:
            annotated_frame = result.render(annotated_frame)  # Annotate the frame
        return annotated_frame

    def process_video(self):
        cap = cv2.VideoCapture(0)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        output_video = cv2.VideoWriter('annotated_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

        while cap.isOpened():
            start_time = time.perf_counter()
            ret, frame = cap.read()
            if not ret:
                break
            annotated_frame = self.score_frame(frame)
            output_video.write(annotated_frame)  # Write the annotated frame to the video

            end_time = time.perf_counter()
            fps = 1 / np.round(end_time - start_time, 3)
            cv2.putText(annotated_frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5)
            cv2.imshow("Annotated Frame", annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        output_video.release()
        cv2.destroyAllWindows()

detection = Async()
detection.process_video()
