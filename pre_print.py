import RPi.GPIO as GPIO

import motor.motor as motor
from RpiMotorLib.RpiMotorLib import StopMotorInterrupt
from switch import switch

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

STEPS_PER_SIDE = motor.STEPS_PER_LOOP / 2 + motor.STEPS_PER_LOOP / 8


def pre_print(enable_hook: bool = True):
    if not switch.is_camera_in_home():
        if enable_hook:
            switch.enable_switch_hook()
        try:
            try:
                motor.motor_go(False, int(STEPS_PER_SIDE))
            except StopMotorInterrupt:
                pass
            else:
                if switch.is_camera_in_home():
                    try:
                        motor.motor_go(True, int(STEPS_PER_SIDE * 2))
                    except StopMotorInterrupt:
                        pass
                    else:
                        raise SystemError
        finally:
            switch.disable_switch_hook()


if __name__ == "__main__":
    pre_print()
