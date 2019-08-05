#!/usr/bin/env python3

'''
This is a class for controlling the stepper motor

Note: the RPM is not entirely accurate
'''

import Adafruit_BBIO.GPIO as GPIO
import rcpy.mpu9250 as mpu9250
from datetime import datetime
import time
import csv
import os

import lcm
from exlcm import battery

from Switch import Switch

# set constants and variables

pin_dir  = 'GP0_3' # GPIO1_25 57
pin_step = 'GP0_4' # GPIO1_17 49

fieldnames = ['time', 'roll', 'pitch', 'yaw',
              'accel_x', 'accel_y', 'accel_z',
              'gyro_x', 'gyro_y', 'gyro_z',
              'mag_x', 'mag_y', 'mag_z',
              'quat', 'head',
              'depth',
              'distance', 'switch']

datetime_format = '%Y%m%d_%H%M%S'


class Stepper2:

  '''
  Initialize the class, setup pins and switch
  '''
  def __init__(self):
    GPIO.setup(pin_dir, GPIO.OUT)
    GPIO.setup(pin_step,  GPIO.OUT)
    print("pins set up")

    self.inches = 0
    self.switch = Switch()

    self.start = time.time()
    
    self.lc = lcm.LCM()

  '''
  Convert inches to degrees using 8 mm per revolution
  '''
  def inches_to_degrees(self, inches):
    return inches/0.3149*360 #8 mm per revolution

  '''
  Convert degrees to inches using 8 mm per revolution
  '''
  def degrees_to_inches(self, degrees):
    return degrees/360*0.3149

  '''
  Helper function
  Rotate the motor for a specified amount of degrees, at a specified rpm,
  in a specified direction
  '''
  def step(self, degrees, rpm, direction):
    sleep_time=0.3/float(rpm)/2
    steps_forward = int(degrees/1.8)
    for x in range(0, steps_forward):
      GPIO.output(pin_step, GPIO.LOW)
      time.sleep(sleep_time)
      GPIO.output(pin_step, GPIO.HIGH)
      time.sleep(sleep_time)
      self.inches += direction*self.degrees_to_inches(1.8)
    self.cleanup()

  '''
  Helper function
  Rotate the motor in an infinite loop at a specified rpm in a specified direction
  Sends data over lcm
  Stops if switch is pressed
  '''
  def step_infinite(self, rpm, direction):
    print("step_infinite")
    sleep_time=0.3/float(rpm)/2
    self.start = time.time()
    
    while True:
      # check switch
      if self.switch.is_changed_state():
        print("switch changed")
        
        #self.inches = 0
        
        # send data one last time so that new switch state is captured
        msg = battery()
        msg.inches = self.inches
        msg.switch = self.switch.state
        msg.timestamp = datetime.strftime(datetime.now(),datetime_format)

        self.lc.publish("battery_data", msg.encode())
        
        self.cleanup()
        
        break

      # step
      GPIO.output(pin_step, GPIO.LOW)
      time.sleep(sleep_time)
      GPIO.output(pin_step, GPIO.HIGH)
      time.sleep(sleep_time)
      self.inches += direction*self.degrees_to_inches(1.8)

      # every 10 Hz send the data over lcm
      if (time.time() - self.start >= 0.1): # 10 Hz
        msg = battery()
        msg.inches = self.inches
        msg.switch = self.switch.state
        msg.timestamp = datetime.strftime(datetime.now(),datetime_format)

        self.lc.publish("battery_data", msg.encode())
        
        self.start = time.time()

  '''
  Function to rotate clockwise at specified rpm and for specified degrees
  '''
  def step_clockwise_degrees(self, degrees, rpm):
    GPIO.output(pin_dir, GPIO.HIGH)
    self.step(degrees, rpm, -1) # back

  '''
  Function to rotate counterclockwise at specified rpm and for specified degrees
  '''
  def step_counterclockwise_degrees(self, degrees, rpm):
    GPIO.output(pin_dir, GPIO.LOW)
    self.step(degrees, rpm, 1) # forward

  '''
  Function to rotate clockwise at specified rpm and for specified inches
  '''
  def step_clockwise_inches(self, inches, rpm):
    degrees = self.inches_to_degrees(inches)
    self.step_clockwise_degrees(degrees, rpm)

  '''
  Function to rotate counterclockwise at specified rpm and for specified inches
  '''
  def step_counterclockwise_inches(self, inches, rpm):
    degrees = self.inches_to_degrees(inches)
    self.step_counterclockwise_degrees(degrees, rpm)

  '''
  Function to rotate clockwise at specified rpm infinitely
  '''
  def step_clockwise_infinite(self, rpm):
    GPIO.output(pin_dir, GPIO.HIGH)
    self.step_infinite(rpm, -1) # back

  '''
  Function to rotate counterclockwise at specified rpm infinitely
  '''
  def step_counterclockwise_infinite(self, rpm):
    GPIO.output(pin_dir, GPIO.LOW)
    self.step_infinite(rpm, 1) # forward

  '''
  Function to update stored traveled inches to specified inches
  '''
  def update_inches(self, inches):
    self.inches = inches

  '''
  Function to return traveled inches stored in the object 
  '''
  def get_inches(self):
    return inches

  '''
  Function to cleanup pins used by the stepper motor
  '''
  def cleanup():
    GPIO.cleanup()

  
