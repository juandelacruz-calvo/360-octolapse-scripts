import time

import RPi.GPIO as GPIO

from motor import motor

SWITCH_PIN = 27

GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def button_pressed_callback(channel):
    print("switch triggered")
    motor.stop_motor()


def enable_switch_hook():
    try:
        GPIO.add_event_detect(SWITCH_PIN, GPIO.FALLING,
                              callback=button_pressed_callback, bouncetime=200)
    except RuntimeError as err:
        print("Error enabling switch: %s" % err)


def disable_switch_hook():
    GPIO.remove_event_detect(SWITCH_PIN)
    time.sleep(0.5)


def is_camera_in_home() -> bool:
    return not GPIO.input(SWITCH_PIN)
