from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import json
from src.video_util import capture_video_stream, load_one_frame

bounding_boxes = []
total_no_of_shown_frames = 0
loaded_bounding_boxes = []

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to input video file")
ap.add_argument("-i", "--import", type=str, required=True,
                help="path to bounding box json file")

args = vars(ap.parse_args())


def load_file_content(path):
    with open(args['import']) as json_file:
        data = json.load(json_file)
    return data


def draw_intial_bounding_boxes(frame):
    for bb in loaded_bounding_boxes:
        object_id = bb['object_id']
        bounding_box = bb['bounding_box']
        frame_no = bb['frame_no']

        if(total_no_of_shown_frames == frame_no):
            
            (startX, startY, w, h) = bounding_box
            endX = startX + w
            endY = startY + h
            cv2.rectangle(frame, (startX, startY),
                          (endX, endY), (255, 0, 0), 2)
            draw_text(frame,
                      center_of_rect(startX, startY, w, h), object_id)


def draw_text(frame, coords, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, str(text), coords, font,
                0.5, (255, 255, 255), 2, cv2.LINE_AA)

def center_of_rect(x, y, w, h):
    centerX = x + 0.5 * w
    centerY = y + 0.5 * h
    return (int(centerX), int(centerY))


def main():
    global total_no_of_shown_frames, loaded_bounding_boxes
    loaded_bounding_boxes = load_file_content(args['import'])
    cv2.namedWindow("Tracker Window")
    video_stream = capture_video_stream(args)

    while True:
        frame = load_one_frame(video_stream, args)
        # Exit if there not video
        if frame is None:
            print("video stream has ended")
            break

        frame = imutils.resize(frame, width=1000)
        total_no_of_shown_frames += 1

        draw_intial_bounding_boxes(frame)
        cv2.imshow("Tracker Window", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            break


if __name__ == "__main__":

    main()
