from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os


paused_frame = None
centroids = []

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to input video file")
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
    initBB = cv2.selectROI("Frame", frame, fromCenter=False,
                           showCrosshair=True)
    (startX, startY, w, h) = initBB
    endX = startX + w
    endY = startY + h
    centroids.append(center_of_rect(startX, startY, w, h))

    # Add trackers here


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


def clear_all_trackers():
    global centroids
    centroids = []


def main():
    global paused_frame

    cv2.namedWindow("Frame")
    video_stream = capture_video_stream()

    while True:
        if paused_frame is not None:
            frame = paused_frame
        else:
            frame = load_one_frame(video_stream)

        frame = imutils.resize(frame, width=1000)
        if frame is None:
            break

        draw_circle(frame)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("p"):
            pause_on_current_frame(frame)
        if key == ord("b"):
            show_roi_selector(frame)
        if key == ord('c'):
            clear_all_trackers()

        if key == 27:
            break


if __name__ == "__main__":
    main()