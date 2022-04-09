import time

import RPi.GPIO as GPIO

from motor import motor

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

SWITCH_PIN = 27


def button_pressed_callback(channel):
    # print("switch triggered")
    motor.stop_motor()
    disable_switch_hook()
    time.sleep(0.5)


def enable_switch_hook():
    try:
        GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        time.sleep(.25)
        GPIO.add_event_detect(SWITCH_PIN, GPIO.FALLING,
                              callback=button_pressed_callback, bouncetime=50)
    except RuntimeError as err:
        print("Error enabling switch: %s" % err)


def disable_switch_hook():
    GPIO.remove_event_detect(SWITCH_PIN)


def is_camera_in_home() -> bool:
    return not GPIO.input(SWITCH_PIN)
