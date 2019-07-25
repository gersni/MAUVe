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

imu = mpu9250.IMU(enable_dmp=True,
                  dmp_sample_rate=100,
                  enable_magnetometer=True)

fieldnames = ['time', 'roll', 'pitch', 'yaw',
              'accel_x', 'accel_y', 'accel_z',
              'gyro_x', 'gyro_y', 'gyro_z',
              'mag_x', 'mag_y', 'mag_z',
              'quat', 'head',
              'depth',
              'distance', 'switch']

datetime_format = '%Y%m%d_%H%M%S'

if not os.path.exists("log.csv"):
  csvfile = open('log.csv', 'w')
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
else:
  csvfile = open('log.csv', 'a')
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


start = time.time()

while True:
  if switch.is_changed_state():
    stepper.inches = 0
    break

  stepper.step_counterclockwise_degrees(1.8,100)

  if (time.time() - start >= 0.1): # 10 Hz
    imu_out = imu.read()
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
                     'distance':stepper.inches,
                     'switch':switch.state})
    start = time.time()



csvfile.close()


'''
while True:
  if switch.is_changed_state():
    print("pressed")
    break
  stepper.step_clockwise_degrees(360, 20)
'''