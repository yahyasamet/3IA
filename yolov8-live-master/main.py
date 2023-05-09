import cv2
import argparse

from ultralytics import YOLO
import supervision as sv
import numpy as np
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import time
import pyttsx3
import threading



def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", 
        default=[1280, 720], 
        nargs=2, 
        type=int
    )
    args = parser.parse_args()
    return args

def speak(text):
    engine = pyttsx3.init()
    engine.say("I see a "+text)
    engine.runAndWait()


def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model = YOLO("trolley.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )


    while True:
        ret, frame = cap.read()

        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)

        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _
            in detections
        ]
        names = [label.split()[0] for label in labels]
        if names:
            thread = threading.Thread(target=speak, args=names,)
            thread.start()
        
        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections, 
            labels=labels
        )
           
        
        cv2.imshow("yahya", frame)
        
        
        if (cv2.waitKey(30) == 27):
            break


if __name__ == "__main__":
    main()