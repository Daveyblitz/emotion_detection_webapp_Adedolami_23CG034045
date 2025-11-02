from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
import cv2
from deepface import DeepFace
import os
import threading
import time

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return redirect(request.url)
    
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)

    # Save the uploaded image
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    # Analyze emotion (handle dict or list return types)
    result = DeepFace.analyze(image_path, actions=['emotion'], enforce_detection=False)
    emotion = result[0].get('dominant_emotion') if isinstance(result, list) else result.get('dominant_emotion')

    return render_template('result.html', emotion=emotion, image_path=image_path)

@app.route('/live')
def live():
    return render_template('live.html')

# Camera manager (start/stop on demand)
class CameraManager:
    def __init__(self, index=0, analyze_interval=20):
        self.index = index
        self.analyze_interval = analyze_interval
        self.cap = None
        self.thread = None
        self.running = False
        self.lock = threading.Lock()
        self.frame = None
        self.last_emotion = "Unknown"

    def start(self):
        if self.running:
            return True
        self.cap = cv2.VideoCapture(self.index)
        if not self.cap.isOpened():
            return False
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        return True

    def _run(self):
        frame_count = 0
        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    break
                frame_count += 1
                # analyze less frequently
                if frame_count % self.analyze_interval == 0:
                    try:
                        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                        if isinstance(result, list):
                            self.last_emotion = result[0].get('dominant_emotion') or self.last_emotion
                        else:
                            self.last_emotion = result.get('dominant_emotion') or self.last_emotion
                    except Exception:
                        # ignore analysis errors
                        pass
                cv2.putText(frame, f'Mood: {self.last_emotion}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                with self.lock:
                    self.frame = frame.copy()
                time.sleep(0.01)
        finally:
            self.running = False
            if self.cap:
                self.cap.release()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        with self.lock:
            self.frame = None

    def get_frame(self):
        with self.lock:
            return None if self.frame is None else self.frame.copy()

camera = CameraManager(index=0, analyze_interval=20)

@app.route('/start_stream', methods=['POST'])
def start_stream():
    ok = camera.start()
    if not ok:
        return jsonify({"ok": False, "error": "Camera not available"}), 503
    return jsonify({"ok": True})

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    camera.stop()
    return jsonify({"ok": True})

def gen_frames():
    # If camera isn't running, yield nothing (client will handle)
    while camera.running:
        frame = camera.get_frame()
        if frame is None:
            time.sleep(0.05)
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    # When camera stops, send nothing more

@app.route('/video_feed')
def video_feed():
    if not camera.running:
        return ("", 503)
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # threaded so the stream generator won't block other requests
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)