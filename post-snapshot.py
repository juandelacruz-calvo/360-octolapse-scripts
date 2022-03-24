#!/usr/bin/env python3

import RPi.GPIO as GPIO
import sys
from RpiMotorLib.RpiMotorLib import StopMotorInterrupt

import motor.motor as motor

# SNAPSHOT_NUMBER=$1
# DELAY_SECONDS=$2
# DATA_DIRECTORY=$3
# SNAPSHOT_DIRECTORY=$4
# SNAPSHOT_FILENAME=$5
# SNAPSHOT_FULL_PATH=$6


SWITCH_PIN = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def button_pressed_callback(channel):
    motor.stop_motor()


def main():
    snapshot_number = int(sys.argv[1])
    GPIO.add_event_detect(SWITCH_PIN, GPIO.FALLING,
                          callback=button_pressed_callback, bouncetime=100)

    try:
        # Add 10 to let the micro switch do the jobs
        motor.move_motor(snapshot_number, False)
    except StopMotorInterrupt:
        pass
    else:
        raise SystemError
    finally:
        motor.disable_stepper()


main()
