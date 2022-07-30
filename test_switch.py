import time

from switch import switch


def test_something():
    switch.enable_switch_hook()
    while True:
        if switch.is_camera_in_home():
            print("triggered")
            time.sleep(0.05)


if __name__ == "__main__":
    test_something()
