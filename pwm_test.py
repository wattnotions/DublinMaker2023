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

try:
    while True:
        # Get pulse length
        pulse_length = input("Enter the pulse length in ms (1.0 to 2.0): ")
        
        # Check if input is valid
        try:
            pulse_length = float(pulse_length)
        except ValueError:
            print("Invalid input! Please enter a number between 1.0 and 2.0.")
            continue
        
        # Check if pulse length is in the valid range
        if not 1.0 <= pulse_length <= 2.0:
            print("Pulse length should be between 1.0 ms and 2.0 ms.")
            continue
        
        # Convert pulse length to duty cycle
        # Pulse length of 1ms corresponds to a duty cycle of 5%,
        # and pulse length of 2ms corresponds to a duty cycle of 10%.
        duty_cycle = pulse_length / 20.0 * 100.0
        
        # Change the duty cycle
        pwm.ChangeDutyCycle(duty_cycle)
        
except KeyboardInterrupt:
    # Stop the PWM signal
    pwm.stop()

    # Clean up all GPIOs
    GPIO.cleanup()

    print("\nStopped by User")

