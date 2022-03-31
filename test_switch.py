import time

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
        if switch.is_camera_in_home():
            print("triggered")
            time.sleep(0.05)


if __name__ == "__main__":
    test_something()
