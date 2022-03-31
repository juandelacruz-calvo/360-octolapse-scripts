import time
from random import randint

import pre_print
from switch import switch

ITEMS_PER_LINE = 8

steps_results = list()

for i in range(800):
    steps_results.append({True: 0, False: 0})


def post_result(steps, success):
    steps_results[steps][success] = steps_results[steps][success] + 1


def test_something():
    switch.enable_switch_hook()
    while True:
        print(switch.is_camera_in_home())


if __name__ == "__main__":
    test_something()
