import time

from AdvPiStepper.advpistepper.common import DECELERATION_RATE, ACCELERATION_RATE, MAX_SPEED
from AdvPiStepper.advpistepper.driver_step_dir_generic import DriverStepDirGeneric
from AdvPiStepper.advpistepper.stepper import AdvPiStepper

EN_pin = 24  # enable pin (LOW to enable)

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(EN_pin, GPIO.OUT)  # set enable pin as output
GPIO.output(EN_pin, GPIO.LOW)

driver = DriverStepDirGeneric(step_pin=23, dir_pin=22, parameters={
    DECELERATION_RATE: 1000,
    ACCELERATION_RATE: 500,
    MAX_SPEED: 2000
})
stepper = AdvPiStepper(driver)
stepper.move(600, block=True)
time.sleep(0.25)
GPIO.output(EN_pin, GPIO.HIGH)
