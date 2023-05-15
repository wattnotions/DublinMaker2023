import time
import Adafruit_ADS1x15  # Install the Adafruit ADS1x15 library (pip install adafruit-ads1x15)

# Create an ADS1115 ADC object
adc = Adafruit_ADS1x15.ADS1115()

# Configure ADC settings
#adc.set_mode(Adafruit_ADS1x15.Mode.CONTINUOUS)  # Set the operating mode (CONTINUOUS or SINGLE)
#adc.set_gain(16)  # Set the gain (options: 2/4/8/16)
#adc.set_data_rate(250)  # Set the data rate (options: 8/16/32/64/128/250/475/860)



# Set the gain (input range) of the ADC (options: 2/4/8/16)
GAIN = 2

# Main loop
while True:
    # Read the ADC value for channel 0
    adc_value = adc.read_adc(0, gain=GAIN)
    
    # Print the ADC value
   # print("ADC Value: {}".format(adc_value))
    print(adc_value)
    # Delay for 1 second
    time.sleep(0.05)

