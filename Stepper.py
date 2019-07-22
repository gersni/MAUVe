#!/usr/bin/env python3

import Adafruit_BBIO.GPIO as GPIO
import time

pin_dir  = 'GP0_3' # GPIO1_25 57
pin_step = 'GP0_4' # GPIO1_17 49

class Stepper:

  def __init__(self):
    GPIO.setup(pin_dir, GPIO.OUT)
    GPIO.setup(pin_step,  GPIO.OUT)
    print("pins set up")
    self.inches = 0

  def inches_to_degrees(self, inches):
    return inches/0.3149*360 #8 mm per revolution

  def degrees_to_inches(self, degrees):
    return degrees/360*0.3149

  def step(self, degrees, rpm, direction):
    sleep_time=0.3/float(rpm)/2
    steps_forward = int(degrees/1.8)
    for x in range(0, steps_forward):
      GPIO.output(pin_step, GPIO.LOW)
      time.sleep(sleep_time)
      GPIO.output(pin_step, GPIO.HIGH)
      time.sleep(sleep_time)
      self.inches += direction*self.degrees_to_inches(1.8)

  def step_infinite(self, rpm, direction):
    sleep_time=0.3/float(rpm)/2
    x = 0
    while True:
      GPIO.output(pin_step, GPIO.LOW)
      time.sleep(sleep_time)
      GPIO.output(pin_step, GPIO.HIGH)
      time.sleep(sleep_time)
      self.inches += direction*self.degrees_to_inches(1.8)
      x += 1

  def step_clockwise_degrees(self, degrees, rpm):
    GPIO.output(pin_dir, GPIO.HIGH)
    self.step(degrees, rpm, -1) # back

  def step_counterclockwise_degrees(self, degrees, rpm):
    GPIO.output(pin_dir, GPIO.LOW)
    self.step(degrees, rpm, 1) # forward

  def step_clockwise_inches(self, inches, rpm):
    degrees = self.inches_to_degrees(inches)
    self.step_clockwise_degrees(degrees, rpm)

  def step_counterclockwise_inches(self, inches, rpm):
    degrees = self.inches_to_degrees(inches)
    self.step_counterclockwise_degrees(degrees, rpm)

  def step_clockwise_infinite(self, rpm):
    GPIO.output(pin_dir, GPIO.HIGH)
    self.step_infinite(rpm, -1) # back

  def step_counterclockwise_infinite(self, rpm):
    GPIO.output(pin_dir, GPIO.LOW)
    self.step_infinite(rpm, 1) # forward

  def update_inches(self, inches):
    self.inches = inches

  def get_inches(self):
    return inches

  def cleanup():
    GPIO.cleanup()

