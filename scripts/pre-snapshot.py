import sys

import motor.motor as motor


# SNAPSHOT_NUMBER=$1
# DELAY_SECONDS=$2
# DATA_DIRECTORY=$3
# SNAPSHOT_DIRECTORY=$4
# SNAPSHOT_FILENAME=$5
# SNAPSHOT_FULL_PATH=$6


def pre_snapshot(snapshot_number: int):
    motor.move_motor(snapshot_number, True)


if __name__ == "__main__":
    pre_snapshot(int(sys.argv[1]))
