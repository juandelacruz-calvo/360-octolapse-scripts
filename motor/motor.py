import RPi.GPIO as GPIO
import time
from RpiMotorLib import RpiMotorLib

FAST_SPEED = .0005
SLOW_SPEED = .001
EXTRA_STEPS_RETURNING = 25
SAFETY_DISTANCE = 150

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

    GPIO.output(EN_pin, GPIO.LOW)  # pull enable to low to enable motor
    stepper.stop_motor = False
    if pre_snapshot:
        move_pre_snapshot(clockwise, scaled_steps)
    else:
        # Add a safety net to make sure the switch works
        scaled_steps = scaled_steps + EXTRA_STEPS_RETURNING
        move_post_snapshot(clockwise, scaled_steps)
    time.sleep(0.25)
    disable_stepper()


def move_pre_snapshot(clockwise, scaled_steps):
    stepper.motor_go(clockwise,  # True=Clockwise, False=Counter-Clockwise
                     "Full",  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                     scaled_steps,  # number of steps
                     .0005,  # step delay [sec]
                     False,  # True = print verbose output
                     .05)  # initial delay [sec]


def move_post_snapshot(clockwise, scaled_steps):

    if scaled_steps > SAFETY_DISTANCE:
        stepper.motor_go(clockwise,  # True=Clockwise, False=Counter-Clockwise
                         "Full",  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         scaled_steps - SAFETY_DISTANCE,  # number of steps
                         FAST_SPEED,  # step delay [sec]
                         False,  # True = print verbose output
                         .05)  # initial delay [sec]
        stepper.motor_go(clockwise,  # True=Clockwise, False=Counter-Clockwise
                         "Full",  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         SAFETY_DISTANCE,  # number of steps
                         SLOW_SPEED,  # step delay [sec]
                         False,  # True = print verbose output
                         0)  # initial delay [sec]
    else:
        stepper.motor_go(clockwise,  # True=Clockwise, False=Counter-Clockwise
                         "Full",  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         scaled_steps,  # number of steps
                         SLOW_SPEED,  # step delay [sec]
                         False,  # True = print verbose output
                         .05)  # initial delay [sec]


def stop_motor():
    stepper.motor_stop()


def disable_stepper():
    GPIO.output(EN_pin, GPIO.HIGH)
