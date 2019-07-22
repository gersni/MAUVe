#!/usr/bin/env python3

from datetime import datetime
import rcpy.mpu9250 as mpu9250
import time
import csv
import os

from Stepper import Stepper
from Switch import Switch
#from Servo import Servo


stepper = Stepper()
switch = Switch()
#servo = Servo()

#imu = mpu9250.initialize(enable_dmp=True,
#                         dmp_sample_rate=10,
#                         enable_fusion=True,
#                         enable_magnetometer=True)


fieldnames = ['time', 'roll', 'pitch', 'yaw',
              'accel_x', 'accel_y', 'accel_z',
              'gyro_x', 'gyro_y', 'gyro_z',
              'mag_x', 'mag_y', 'mag_z',
              'quat', 'head',
              'depth', 'temperature', 
              'distance', 'switch']

datetime_format = '%Y%m%d_%H%M%S'

if not os.path.exists("log.csv"):
  csvfile = open('log.csv', 'w')
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
else:
  csvfile = open('log.csv', 'a')
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


for x in range(10):
  #imu_out = imu.read()
  if switch.is_changed_state():
    stepper.inches = 0
  stepper.step_counterclockwise_degrees(360,100)
  writer.writerow({'time':datetime.strftime(datetime.now(),datetime_format),
                   'roll':'',
                   'pitch':'',
                   'yaw':'',
                   'accel_x':'',
                   'accel_y':'',
                   'accel_z':'',
                   'gyro_x':'',
                   'gyro_y':'',
                   'gyro_z':'',
                   'mag_x':'',
                   'mag_y':'',
                   'mag_z':'',
                   'quat':'',
                   'head':'',
                   'depth':'',
                   'temperature':'',
                   'distance':stepper.inches,
                   'switch':switch.state})
  time.sleep(0.1) # 10Hz


csvfile.close()


'''
while True:
  if switch.is_changed_state():
    print("pressed")
    break
  stepper.step_clockwise_degrees(360, 20)
'''