import sys

import motor.motor as motor



def pre_snapshot(snapshot_number: int):
    motor.move_motor(snapshot_number, True)
