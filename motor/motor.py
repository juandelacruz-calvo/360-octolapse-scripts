import time

import RPi.GPIO as GPIO

from RpiMotorLib import RpiMotorLib

MULTIPLIER_PAUSE_BETWEEN_STEPS = 1.05

FAST_SPEED = .0004
SLOW_SPEED = .0004
EXTRA_STEPS_RETURNING = 20
SAFETY_DISTANCE = 50  # Has to be multiple of 5

direction = 22  # Direction (DIR) GPIO Pin
step = 23  # Step GPIO Pin
EN_pin = 24  # enable pin (LOW to enable)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(EN_pin, GPIO.OUT)  # set enable pin as output
GPIO.output(EN_pin, GPIO.HIGH)

stepper = RpiMotorLib.A4988Nema(direction, step, (-1, -1, -1), "DRV8825")

STEPS_PER_LOOP = 4000


def move_motor(steps, pre_snapshot):
    clockwise = True

    scaled_steps = steps * 5

    # First skip extra loops
    scaled_steps = scaled_steps % STEPS_PER_LOOP

    # Second check if it's easier to go left than righted
    if scaled_steps > (STEPS_PER_LOOP / 2):
        clockwise = False
        scaled_steps = STEPS_PER_LOOP - scaled_steps

    # Reverse the step of it's post snapshot
    clockwise = not clockwise if pre_snapshot is False else clockwise
    try:

        if pre_snapshot:
            take_snapshot(clockwise, scaled_steps)
        else:
            # Add a safety net to make sure the switch works
            scaled_steps = scaled_steps + EXTRA_STEPS_RETURNING
            take_snapshot(clockwise, scaled_steps)
    finally:
        time.sleep(0.25)
        disable_stepper()


def take_snapshot(clockwise, scaled_steps):
    if scaled_steps > SAFETY_DISTANCE:
        motor_go(clockwise, scaled_steps - SAFETY_DISTANCE)
        motor_decrease_speed(clockwise, SAFETY_DISTANCE)
    else:
        motor_decrease_speed(clockwise, scaled_steps)


def motor_go(clockwise: bool, absolute_steps: int, fast: bool = True, initial_delay: float = .05):
    GPIO.output(EN_pin, GPIO.LOW)  # pull enable to low to enable motor
    stepper.motor_go(clockwise,  # True=Clockwise, False=Counter-Clockwise
                     "Full",  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                     absolute_steps,  # number of steps
                     FAST_SPEED if fast else SLOW_SPEED,  # step delay [sec]
                     False,  # True = print verbose output
                     initial_delay)  # initial delay [sec]


def motor_decrease_speed(clockwise: bool, absolute_steps: int):
    GPIO.output(EN_pin, GPIO.LOW)  # pull enable to low to enable motor
    base_pause_value = SLOW_SPEED
    for i in range(absolute_steps):
        base_pause_value = base_pause_value * MULTIPLIER_PAUSE_BETWEEN_STEPS
        print("Pause between steps: %f" % base_pause_value)
        stepper.motor_go(clockwise,  # True=Clockwise, False=Counter-Clockwise
                         "Full",  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         1,  # number of steps
                         base_pause_value,
                         False,  # True = print verbose output
                         0)  # initial delay [sec]


def stop_motor():
    stepper.motor_stop()


def disable_stepper():
    GPIO.output(EN_pin, GPIO.HIGH)
