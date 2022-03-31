import sys

import RPi.GPIO as GPIO

import motor.motor as motor
import pre_print
from RpiMotorLib.RpiMotorLib import StopMotorInterrupt
from switch import switch

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


def post_snapshot(snapshot_number: int):
    switch.enable_switch_hook()

    raised_stop = switch.is_camera_in_home()
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


if __name__ == "__main__":
    post_snapshot(int(sys.argv[1]))
