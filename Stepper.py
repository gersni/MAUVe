import Adafruit_BBIO.GPIO as GPIO
import time

pin_dir = 'GP0_3'  # GPIO1_25 57
pin_step = 'GP0_4' # GPIO1_17 49

class Stepper:

  def __init__(self):
    GPIO.setup(pin_dir, GPIO.OUT)
    GPIO.setup(pin_step,  GPIO.OUT)
    print("pins set up")

  def step(self, degrees, rpm):
    sleep_time=0.3/float(rpm)/2
    steps_forward = int(degrees/1.8)
    for x in range(0, steps_forward):
      GPIO.output(pin_step, GPIO.LOW)
      time.sleep(sleep_time)
      GPIO.output(pin_step, GPIO.HIGH)
      time.sleep(sleep_time)

  def step_clockwise_degrees(self, degrees, rpm):
    GPIO.output(pin_dir, GPIO.HIGH)
    self.step(degrees, rpm)

  def step_counterclockwise_degrees(self, degrees, rpm):
    GPIO.output(pin_dir, GPIO.LOW)
    self.step(degrees, rpm)

  def step_clockwise_inches(self, inches, rpm):
    degrees = inches/0.063*360 #0.063 inches per revolution
    self.step_clockwise_degrees(degrees, rpm)

  def step_counterclockwise_inches(self, inches, rpm):
    degrees = inches/0.063*360 #0.063 inches per revolution
    self.step_counterclockwise_degrees(degrees, rpm)
