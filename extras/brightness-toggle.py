import RPi.GPIO as GPIO
import subprocess
import time

# GPIO pin numbers
BUTTON_PIN = 17                                          #Button Pin
PWM_PIN = 18                                             #Display PWM (LED) Pin
# PWM values for brightness levels
BRIGHTNESS_VALUES = [0, 20, 40, 60, 80, 100]

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PWM_PIN, GPIO.OUT)
pwm = GPIO.PWM(PWM_PIN, 245)

current_brightness = 0
pwm_started = False

def button_pressed(channel):
    global current_brightness
    global pwm_started

    if not pwm_started:
        pwm.start(0)
        pwm_started = True

    index = BRIGHTNESS_VALUES.index(current_brightness)
    next_index = (index + 1) % len(BRIGHTNESS_VALUES)
    next_brightness = BRIGHTNESS_VALUES[next_index]
    pwm.ChangeDutyCycle(next_brightness)
    current_brightness = next_brightness

    # Stop the pwm.service when button is pressed
    subprocess.call(['systemctl', 'stop', 'pwm.service'])

GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=200)

while True:
    time.sleep(1)
