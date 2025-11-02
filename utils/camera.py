import cv2

def start_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open video device")

    return cap

def capture_frame(cap):
    ret, frame = cap.read()
    if not ret:
        raise Exception("Could not read frame from camera")
    
    return frame

def release_camera(cap):
    cap.release()