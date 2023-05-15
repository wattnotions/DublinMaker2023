import time
import Adafruit_ADS1x15  # Install the Adafruit ADS1x15 library (pip install adafruit-ads1x15)
import numpy as np

# Create an ADS1115 ADC object
adc = Adafruit_ADS1x15.ADS1115()

# Configure ADC settings
#adc.set_mode(Adafruit_ADS1x15.Mode.CONTINUOUS)  # Set the operating mode (CONTINUOUS or SINGLE)
#adc.set_gain(16)  # Set the gain (options: 2/4/8/16)
#adc.set_data_rate(250)  # Set the data rate (options: 8/16/32/64/128/250/475/860)

import RPi.GPIO as GPIO

# Use GPIO numbering
GPIO.setmode(GPIO.BCM)

# Set the GPIO12 as output
pin = 12
GPIO.setup(pin, GPIO.OUT)

# Set frequency to 50Hz (period of 20ms)
pwm = GPIO.PWM(pin, 50)

# Start PWM with 0% duty cycle (off)
pwm.start(0)
GAIN=2
try:
    while True:
        

        # Read the ADC value for channel 0
        adc_value = adc.read_adc(0, gain=GAIN)
        
        # Map the ADC value to the desired range
        mapped_value = np.interp(adc_value, [3000, 10000], [1.3, 1.2])
        
        # Print the ADC value
       
        print(mapped_value, adc_value)
        # Delay for 1 second
        
        duty_cycle = mapped_value / 20.0 * 100.0


        # Change the duty cycle
        pwm.ChangeDutyCycle(duty_cycle)
        
        time.sleep(0.05)

except KeyboardInterrupt:
    # Stop the PWM signal
    pwm.stop()

    # Clean up all GPIOs
    GPIO.cleanup()

    print("\nStopped by User")



