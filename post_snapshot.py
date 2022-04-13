import sys

import motor.motor as motor
import pre_print
from RpiMotorLib.RpiMotorLib import StopMotorInterrupt
from switch import switch


def post_snapshot(snapshot_number: int):
    switch.enable_switch_hook()

    is_homed = switch.is_camera_in_home()
    if not is_homed:
        try:
            # Add 10 to let the micro switch do the jobs
            motor.move_motor(snapshot_number, False)
        except StopMotorInterrupt:
            pass
        else:
            try:
                pre_print.pre_print(True, False)
            finally:
                motor.disable_stepper()


if __name__ == "__main__":
    post_snapshot(int(sys.argv[1]))
