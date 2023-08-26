import time
import RPi.GPIO as GPIO
from gpiozero import Servo
import threading

class EyesController:

    def __init__(self, pin=19):
        self.eyes_servo = Servo(pin)
        self.eyes_setpoint = 90
        self.eyes_thread_instance = threading.Thread(target=self.eyes_thread_func, name="eyes")
        self.eyes_thread_instance.daemon = True
        self.eyes_thread_instance.start()

    @staticmethod
    def map_angle_to_value(angle):
        return (angle / 90.0) - 1.0

    def eyes_thread_func(self):
        try:
            while True:
                self.eyes_servo.value = self.map_angle_to_value(self.eyes_setpoint)
                print(self.eyes_setpoint)
                time.sleep(0.1)  # Adjust the sleep interval as needed
        except KeyboardInterrupt:
            self.eyes_servo.close()
            print("Eyes thread stopped.")

        except Exception as e:
            print(e)

    def set_eyes_setpoint(self, value):
        self.eyes_setpoint = value

    def animate_eyes(self, delay=0.01):
        self.eyes_setpoint = 109
        while self.eyes_setpoint > 10:
            self.eyes_setpoint -= 1
           # print(eyes_setpoint)
            time.sleep(delay)
        while self.eyes_setpoint < 110:
            self.eyes_setpoint += 1
            time.sleep(delay)

if __name__ == "__main__":
    eyes = EyesController()
    try:
        while True:
            eyes.animate_eyes()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nMain program stopped.")
