#!/usr/bin/env python3
import RPi.GPIO as GPIO
from RpiMotorLib.RpiMotorLib import StopMotorInterrupt

import motor.motor as motor

SWITCH_PIN = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def button_pressed_callback(channel):
    motor.stop_motor()


def main():
    GPIO.add_event_detect(SWITCH_PIN, GPIO.FALLING,
                          callback=button_pressed_callback, bouncetime=100)

    raised_stop = GPIO.input(SWITCH_PIN)

    if raised_stop:
        try:
            motor.move_motor(int(motor.STEPS_PER_LOOP / 2), False)
        except StopMotorInterrupt:
            raised_stop = True

        if not raised_stop:
            try:
                motor.move_motor(int(motor.STEPS_PER_LOOP / 2), True)
            except StopMotorInterrupt:
                pass
            else:
                raise SystemError
            finally:
                motor.disable_stepper()


main()
