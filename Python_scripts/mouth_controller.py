import time
import Adafruit_ADS1x15
import numpy as np
import RPi.GPIO as GPIO
import threading


class PWMController(threading.Thread):

    def __init__(self, pin=12, gain=2):
        super(PWMController, self).__init__()
        self.pin = pin
        self.gain = gain
        self.adc = Adafruit_ADS1x15.ADS1115()
        self._stop_event = threading.Event()

        # Initialize the GPIO settings
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0)
        self.pwm_started=1

    def run(self):
        try:
            while not self._stop_event.is_set():
                adc_value = self.adc.read_adc(0, gain=self.gain)
                mapped_value = np.interp(adc_value, [3000, 10000], [1.4, 1.2])
                #print(mapped_value, adc_value)

                if adc_value<10:
                    self.pwm.ChangeDutyCycle(0)
                else:
                    duty_cycle = mapped_value / 20.0 * 100.0
                    self.pwm.ChangeDutyCycle(duty_cycle)
                    time.sleep(0.05)

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self._stop_event.set()
        self.pwm.stop()
        GPIO.cleanup()
        print("\nStopped by User")
