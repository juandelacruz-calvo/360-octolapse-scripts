import time
from random import randint

import pre_print

ITEMS_PER_LINE = 8

steps_results = list()

for i in range(800):
    steps_results.append({True: 0, False: 0})


def post_result(steps, success):
    steps_results[steps][success] = steps_results[steps][success] + 1


def test_something():
    print("call pre print")
    pre_print.pre_print()
    print("Starting script")
    while True:
        steps = randint(0, 799)
        print("Random steps: %d" % steps)
        try:
            import pre_snapshot
            pre_snapshot.pre_snapshot(steps)
            import post_snapshot
            post_snapshot.post_snapshot(steps)
            post_result(steps, True)

            print("--------------------\n", end=None)
            line = ITEMS_PER_LINE
            for index, value in enumerate(steps_results):
                if not value[True] == 0 or not value[False] == 0:
                    line -= 1
                    print("%d => \tS: %d\tF: %d\t" % (index, value[True], value[False]),
                          end='\n' if line == 0 else '')
                    if line == 0:
                        line = ITEMS_PER_LINE

            print("\n--------------------", end=None)
        except SystemError:
            post_result(steps, False)

        # time.sleep(3)


if __name__ == "__main__":
    test_something()
