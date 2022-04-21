import RPi.GPIO as GPIO

import motor.motor as motor
from RpiMotorLib.RpiMotorLib import StopMotorInterrupt
from switch import switch

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

STEPS_PER_SIDE = motor.STEPS_PER_LOOP / 2 + motor.STEPS_PER_LOOP / 8


def pre_print(start_anti_clockwise: bool, enable_hook: bool = True):
    if not switch.is_camera_in_home():
        if enable_hook:
            switch.enable_switch_hook()
        try:
            try:
                motor.motor_go(not start_anti_clockwise, int(STEPS_PER_SIDE))
            except StopMotorInterrupt:
                pass
            else:
                if switch.is_camera_in_home():
                    try:
                        motor.motor_go(start_anti_clockwise, int(STEPS_PER_SIDE * 2))
                    except StopMotorInterrupt:
                        pass
                    else:
                        raise SystemError
        finally:
            switch.disable_switch_hook()
            if enable_hook:
                motor.disable_stepper()


if __name__ == "__main__":
    pre_print(True)
