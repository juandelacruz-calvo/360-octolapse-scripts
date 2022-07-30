import RPi.GPIO as GPIO
import time

from motor import motor

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

SWITCH_PIN = 27
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def button_pressed_callback(channel):
    print("switch trigger")
    if is_camera_in_home():  # Double check the event is valid
        motor.stop_motor()
        disable_switch_hook()
        time.sleep(.5)


def enable_switch_hook():
    try:
        GPIO.add_event_detect(SWITCH_PIN, GPIO.FALLING,
                              callback=button_pressed_callback, bouncetime=5)
        time.sleep(.5)
    except RuntimeError as err:
        print("Error enabling switch: %s" % err)


def disable_switch_hook():
    GPIO.remove_event_detect(SWITCH_PIN)


def is_camera_in_home() -> bool:
    return not GPIO.input(SWITCH_PIN)
