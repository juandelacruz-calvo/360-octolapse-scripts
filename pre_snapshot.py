#!/usr/bin/env python3

import sys

import motor.motor as motor


def pre_snapshot(snapshot_number: int):
    motor.move_motor(snapshot_number, True)


if __name__ == "__main__":
    pre_snapshot(int(sys.argv[1]))
