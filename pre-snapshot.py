#!/usr/bin/env python3

import sys

import motor.motor as motor


# SNAPSHOT_NUMBER=$1
# DELAY_SECONDS=$2
# DATA_DIRECTORY=$3
# SNAPSHOT_DIRECTORY=$4
# SNAPSHOT_FILENAME=$5
# SNAPSHOT_FULL_PATH=$6


def main():
    snapshot_number = int(sys.argv[1])
    motor.move_motor(snapshot_number, True)


main()
