#!/usr/bin/env python3

import Adafruit_BBIO.GPIO as GPIO
import rcpy.mpu9250 as mpu9250
from datetime import datetime
import time
import csv
import os

import lcm
from exlcm import battery

from Switch import Switch

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

  def __init__(self):
    GPIO.setup(pin_dir, GPIO.OUT)
    GPIO.setup(pin_step,  GPIO.OUT)
    print("pins set up")

    self.inches = 0
    self.switch = Switch()

    self.start = time.time()
    self.imu = mpu9250.IMU(enable_dmp=True,
                           dmp_sample_rate=200,
                           enable_magnetometer=True)

    # init csv
    if not os.path.exists("log.csv"):
      self.csvfile = open('log.csv', 'w')
      self.writer = csv.DictWriter(self.csvfile, fieldnames=fieldnames)
      self.writer.writeheader()
    else:
      self.csvfile = open('log.csv', 'a')
      self.writer = csv.DictWriter(self.csvfile, fieldnames=fieldnames)


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
    print("step_infinite")
    sleep_time=0.3/float(rpm)/2
    self.start = time.time()
    while True:
      # check switch


      GPIO.output(pin_step, GPIO.LOW)
      time.sleep(sleep_time)
      GPIO.output(pin_step, GPIO.HIGH)
      time.sleep(sleep_time)
      self.inches += direction*self.degrees_to_inches(1.8)

      if (time.time() - self.start >= 0.1): # 10 Hz
        #msg = battery()
        #msg.inches = self.inches
        #msg.switch = self.switch
        '''if self.switch.is_changed_state():
          print("switch changed")
          self.inches = 0
          break
        '''
        self.start = time.time()


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

  def write_csv(self, writer, imu_out):
    writer.writerow({'time':datetime.strftime(datetime.now(),datetime_format),
                     'pitch':imu_out['tb'][0],
                     'roll':imu_out['tb'][1],
                     'yaw':imu_out['tb'][2],
                     'accel_x':imu_out['accel'][0],
                     'accel_y':imu_out['accel'][1],
                     'accel_z':imu_out['accel'][2],
                     'gyro_x':imu_out['gyro'][0],
                     'gyro_y':imu_out['gyro'][1],
                     'gyro_z':imu_out['gyro'][2],
                     'mag_x':imu_out['mag'][0],
                     'mag_y':imu_out['mag'][1],
                     'mag_z':imu_out['mag'][2],
                     'quat':str(imu_out['quat']),
                     'head':imu_out['head'],
                     'depth':'depth',
                     'distance':self.inches,
                     'switch':self.switch.state})

