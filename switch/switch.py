import RPi.GPIO as GPIO

from motor import motor

SWITCH_PIN = 27

GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def enable_switch_hook():
    try:
        GPIO.add_event_detect(SWITCH_PIN, GPIO.FALLING,
                              callback=button_pressed_callback, bouncetime=100)
    except RuntimeError as err:
        print("Error enabling switch: %s" % err)


def disable_switch_hook():
    GPIO.remove_event_detect(SWITCH_PIN)


def button_pressed_callback(channel):
    motor.stop_motor()


def is_switch_on() -> bool:
    return GPIO.input(SWITCH_PIN)
