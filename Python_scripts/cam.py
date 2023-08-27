import cv2
import threading
import time

class WebcamStream:
    def __init__(self, eyes_controller, frame_rate=5):
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FPS, frame_rate)  # Set frame rate
        self.running = False
        self.lock = threading.Lock()
        self.coordinates = None
        self.eyes_controller = eyes_controller

        # Load the Haar Cascade classifier for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def start(self):
        self.running = True
        threading.Thread(target=self._stream).start()

    def stop(self):
        self.running = False
        self.video_capture.release()

    def _stream(self):
        while self.running:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            coordinates = self.detect_faces(frame)
            with self.lock:
                self.coordinates = coordinates

            #cv2.imshow("Webcam Stream", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def detect_faces(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if len(faces) > 0:
            x, y, w, h = faces[0]  # Assuming there's only one face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.eyes_controller.set_eyes_setpoint(self.map_face_to_eyes_setpoint(x, y, w, h,frame))
            self.eyes_controller.should_animate.set()  # Signal eyes to animate
            return x, y
        else:
            self.eyes_controller.should_animate.clear()  # Clear signal
            return None

    def map_range(self,value, src_min, src_max, dst_min, dst_max):
        # Check if the value is out of the source range
        if value < src_min:
            return dst_min
        if value > src_max:
            return dst_max

        # Calculate the proportion of the value within the source range
        src_range = src_max - src_min
        dst_range = dst_max - dst_min
        value_scaled = float(value - src_min) / float(src_range)

    # Convert the scaled value to the destination range
        return dst_min + (value_scaled * dst_range)

    def map_face_to_eyes_setpoint(self, x, y, w, h, frame):
        
        
        # Calculate the center of the detected face
        face_center_x = x + w // 2

        # Map the face center x-coordinate to servo value (linear mapping)
       
        eye_servo_val = self.map_range(face_center_x, 20, 500, 20, 120)
        # Ensure servo_value stays within the desired range
        
        print(eye_servo_val, face_center_x)
        return eye_servo_val





if __name__ == "__main__":
    stream = WebcamStream(frame_rate=5)  # Set desired frame rate here
    stream.start()

    try:
        while True:
            with stream.lock:
                coordinates = stream.coordinates
            if coordinates is not None:
                x, y = coordinates
                print(f"Face detected at x: {x}, y: {y}")
                time.sleep(1)
    except KeyboardInterrupt:
        pass

    stream.stop()
