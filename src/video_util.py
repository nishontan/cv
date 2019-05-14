import time
import cv2
from imutils.video import VideoStream

def capture_video_stream(args):
    if not args.get("video", False):
        video_stream = VideoStream(src=0).start()
        time.sleep(1.0)
    else:
        video_stream = cv2.VideoCapture(args["video"])
    return video_stream

def load_one_frame(stream,args):
    frame = stream.read()
    frame = frame[1] if args.get("video", False) else frame
    return frame
