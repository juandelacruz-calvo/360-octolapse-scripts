import RPi.GPIO as GPIO

import motor.motor as motor
from RpiMotorLib.RpiMotorLib import StopMotorInterrupt
from switch import switch

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


def pre_print():
    switch.enable_switch_hook()

    raised_stop = switch.is_switch_on()

    if raised_stop:
        try:
            motor.motor_go(True, int(motor.STEPS_PER_LOOP / 2))
        except StopMotorInterrupt:
            raised_stop = True
        if not raised_stop:
            try:
                motor.move_motor(False, int(motor.STEPS_PER_LOOP / 2))
            except StopMotorInterrupt:
                pass
            else:
                raise SystemError
            finally:
                switch.disable_switch_hook()
                motor.disable_stepper()
        else:
            switch.disable_switch_hook()


if __name__ == "__main__":
    pre_print()
