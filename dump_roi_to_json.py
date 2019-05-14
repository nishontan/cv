from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import json
from src.custom_args_parse import str2bool
from src.bounding_box import BoundingBox

paused_frame = None
centroids = []
bounding_boxes = []

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to input video file")
ap.add_argument("-e", "--export", type=str,default='./output.json', help="path to export")
ap.add_argument("-p", "--paused", type=str2bool, nargs='?',
                const=True, default="yes", help="Pauses on first frame")

args = vars(ap.parse_args())


def capture_video_stream():
    if not args.get("video", False):
        video_stream = VideoStream(src=0).start()
        time.sleep(1.0)
    else:
        video_stream = cv2.VideoCapture(args["video"])
    return video_stream


def load_one_frame(stream):
    frame = stream.read()
    frame = frame[1] if args.get("video", False) else frame
    return frame


def center_of_rect(x, y, w, h):
    centerX = x + 0.5 * w
    centerY = y + 0.5 * h
    return (int(centerX), int(centerY))
    # return (x, y)


def show_roi_selector(frame):
    bb = cv2.selectROI("Frame", frame, fromCenter=False,
                       showCrosshair=True)
    (startX, startY, w, h) = bb
    endX = startX + w
    endY = startY + h
    centroids.append(center_of_rect(startX, startY, w, h))

    bounding_box_uid = len(bounding_boxes)
    frame_number = 1  # todo: make this value dynamic
    bounding_boxes.append(BoundingBox(bounding_box_uid, bb, frame_number))


def save_drawn_bounding_boxes():
    json_string = json.dumps([ob.__dict__ for ob in bounding_boxes])
    with open(args['export'], "w") as text_file:
        print(json_string, file=text_file)


def pause_on_current_frame(frame):
    global paused_frame
    if paused_frame is None:
        paused_frame = frame
    else:
        paused_frame = None


def draw_circle(frame):
    for val in centroids:
        cv2.circle(
            frame, (val[0], val[1]), 4, (0, 255, 0), -1)


def draw_text(frame,coords,text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, str(text), coords, font,
                0.5, (255, 255, 255), 2, cv2.LINE_AA)


def clear_all_trackers():
    global centroids
    centroids = []


def draw_bounding_boxes(frame):
    for obj in bounding_boxes:
        (startX, startY, w, h) = obj.bounding_box
        endX = startX + w
        endY = startY + h
        cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)
        draw_text(frame,
                  center_of_rect(startX, startY, w, h),obj.object_id)


def main():
    global paused_frame

    cv2.namedWindow("Frame")
    video_stream = capture_video_stream()

    while True:
        if paused_frame is not None:
            frame = paused_frame
        else:
            frame = load_one_frame(video_stream)

        # Exit if there not video
        if frame is None:
            print("video stream has ended")
            break

        frame = imutils.resize(frame, width=1000)

        if args["paused"] and paused_frame is None:
            pause_on_current_frame(frame)
            continue

        draw_bounding_boxes(frame)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("p"):
            pause_on_current_frame(frame)
        if key == ord("b"):
            show_roi_selector(frame)
        if key == ord('c'):
            clear_all_trackers()
        if key == ord('s'):
            save_drawn_bounding_boxes()

        if key == 27:
            break


if __name__ == "__main__":
    main()
