import RPi.GPIO as GPIO
import time
import argparse

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 245)       #GPIO Pin 18 for the LED Pin of the Display

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--pwm_value', type=int, help='PWM value')
args = parser.parse_args()

if args.pwm_value == 0:
    pwm_value = args.pwm_value
else:
    try:
        pwm_value = args.pwm_value or int(input("Enter PWM value: "))  # Use command-line argument if provided, otherwise prompt user for input
    except ValueError:
        pwm_value = 0

if pwm_value == 0:
    pwm.stop()
    GPIO.cleanup()
else:
    try:
        pwm.start(pwm_value)

        while True:
            time.sleep(1)  # Add a delay to keep the program running

    except KeyboardInterrupt:
        pwm.stop()  # Clean up PWM on keyboard interrupt
        GPIO.cleanup()  # Reset GPIO configuration
