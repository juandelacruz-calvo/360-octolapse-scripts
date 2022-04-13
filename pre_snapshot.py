#!/usr/bin/env python3

import sys

import motor.motor as motor
import pre_print
from switch import switch


def pre_snapshot(snapshot_number: int):
    is_homed = switch.is_camera_in_home()
    if not is_homed:
        pre_print.pre_print(False, True)

    motor.move_motor(snapshot_number, True)


if __name__ == "__main__":
    pre_snapshot(int(sys.argv[1]))
