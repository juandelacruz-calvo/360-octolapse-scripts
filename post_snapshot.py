import RPi.GPIO as GPIO
from . import pre_print
import sys
from RpiMotorLib.RpiMotorLib import StopMotorInterrupt

import motor.motor as motor

SWITCH_PIN = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def button_pressed_callback(channel):
    motor.stop_motor()


def post_snapshot(snapshot_number: int):
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
            pre_print.pre_print()
            raise SystemError
        finally:
            motor.disable_stepper()
            GPIO.remove_event_detect(SWITCH_PIN)


if __name__ == "__main__":
    post_snapshot(int(sys.argv[1]))
