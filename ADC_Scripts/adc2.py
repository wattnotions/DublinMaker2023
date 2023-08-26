import time
import Adafruit_ADS1x15
import numpy as np
import RPi.GPIO as GPIO
import threading
from gpiozero import Servo

# Create an ADS1115 ADC object
adc = Adafruit_ADS1x15.ADS1115()

# Use GPIO numbering
GPIO.setmode(GPIO.BCM)

# Set the GPIO12 as output
pin = 12
GPIO.setup(pin, GPIO.OUT)

# Set frequency to 50Hz (period of 20ms)
pwm = GPIO.PWM(pin, 50)

# Start PWM with 0% duty cycle (off)
pwm.start(0)

# Create Servo objects for neck and eyes
neck_servo = Servo(13)  # Assuming GPIO pin 17 is used for the neck servo
eyes_servo = Servo(19)  # Assuming GPIO pin 18 is used for the eyes servo

# Initialize global variables for setpoints
neck_setpoint = 90  # Default initial setpoint
eyes_setpoint = 90  # Default initial setpoint

# Thread function for the "mouth" thread
def mouth_thread():
    GAIN = 2
    try:
        while True:
            # Read the ADC value for channel 0
            adc_value = adc.read_adc(0, gain=GAIN)
            
            # Map the ADC value to the desired range
            mapped_value = np.interp(adc_value, [3000, 10000], [1.3, 1.2])
            
            # Print the ADC value
            #print(mapped_value, adc_value)
            
            duty_cycle = mapped_value / 20.0 * 100.0
            
            # Change the duty cycle
            pwm.ChangeDutyCycle(duty_cycle)
            
            time.sleep(0.05)
    except KeyboardInterrupt:
        # Stop the PWM signal
        pwm.stop()

        # Clean up all GPIOs
        GPIO.cleanup()

        print("\nMouth thread stopped.")

# Thread function for the "neck" thread
def neck_thread():
    try:
        while True:
            global neck_setpoint
            neck_servo.value = map_angle_to_value(neck_setpoint)
            time.sleep(0.1)  # Adjust the sleep interval as needed
    except KeyboardInterrupt:
        neck_servo.close()
        print("Neck thread stopped.")

# Thread function for the "eyes" thread
def eyes_thread():
    try:
        while True:
            global eyes_setpoint
            eyes_servo.value = map_angle_to_value(eyes_setpoint)
            time.sleep(0.1)  # Adjust the sleep interval as needed
    except KeyboardInterrupt:
        eyes_servo.close()
        print("Eyes thread stopped.")

# Map angle values from the range [0, 180] degrees to the range [-1, 1]
def map_angle_to_value(angle):
    return (angle / 90.0) - 1.0

# Create and start the "mouth" thread
mouth_thread = threading.Thread(target=mouth_thread, name="mouth")
mouth_thread.daemon = True
mouth_thread.start()

# Create and start the "neck" thread
neck_thread = threading.Thread(target=neck_thread, name="neck")
neck_thread.daemon = True
neck_thread.start()

# Create and start the "eyes" thread
eyes_thread = threading.Thread(target=eyes_thread, name="eyes")
eyes_thread.daemon = True
eyes_thread.start()

# Main program
try:
    while True:
        # Get user input for neck and eyes setpoints
        #neck_setpoint = float(input("Enter neck angle setpoint (0 to 180 degrees): "))
        eyes_setpoint = 109
        delay=0.01
        while eyes_setpoint>10:
            eyes_setpoint = eyes_setpoint-1
            print(eyes_setpoint)
            time.sleep(delay)
        while eyes_setpoint < 110:
            eyes_setpoint +=1
            time.sleep(delay)
        
        time.sleep(0.1)
        
        # Your main program logic here
        # This loop can run concurrently with the threads
        pass
except KeyboardInterrupt:
    print("\nMain program stopped.")
