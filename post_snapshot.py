import sys

import RPi.GPIO as GPIO

import motor.motor as motor
from RpiMotorLib.RpiMotorLib import StopMotorInterrupt

SWITCH_PIN = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

global SWITCH_ON


def button_pressed_callback(channel):
    global SWITCH_ON
    if not SWITCH_ON:
        motor.stop_motor()
    SWITCH_ON = True


def post_snapshot(snapshot_number: int):
    global SWITCH_ON
    SWITCH_ON = False
    GPIO.add_event_detect(SWITCH_PIN, GPIO.FALLING,
                          callback=button_pressed_callback, bouncetime=50)

    raised_stop = GPIO.input(SWITCH_PIN)
    if raised_stop:
        try:
            # Add 10 to let the micro switch do the jobs
            motor.move_motor(snapshot_number, False)
        except StopMotorInterrupt:
            pass
        else:
            raise SystemError
        finally:
            motor.disable_stepper()


if __name__ == "__main__":
    post_snapshot(int(sys.argv[1]))
