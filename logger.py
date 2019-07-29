#!/usr/bin/env python3

from datetime import datetime
import rcpy.mpu9250 as mpu9250
import csv
import os

import lcm
from exlcm import imu
from exlcm import battery

# set constants and variables
fieldnames = ['time', 'roll', 'pitch', 'yaw',
              'accel_x', 'accel_y', 'accel_z',
              'gyro_x', 'gyro_y', 'gyro_z',
              'mag_x', 'mag_y', 'mag_z',
              'quat', 'head',
              'depth',
              'distance', 'switch']

datetime_format = '%Y%m%d_%H%M%S'

inches = 0
switch = 0
duty = 0


# open csv file
if not os.path.exists("log.csv"):
  csvfile = open('log.csv', 'w')
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
else:
  csvfile = open('log.csv', 'a')
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


# handle message
def my_handler(channel, data):
  global inches
  global switch

  #print("Received message on channel \"%s\"" % channel)

  # IMU handling
  if channel == "imu_data":
    msg = imu.decode(data)
    #print("imu   timestamp   = %s" % str(msg.timestamp))
    #print("")

    writer.writerow({'time':datetime.strftime(datetime.now(),datetime_format),
                     'pitch':msg.pitch,
                     'roll':msg.roll,
                     'yaw':msg.yaw,
                     'accel_x':msg.accel_x,
                     'accel_y':msg.accel_y,
                     'accel_z':msg.accel_z,
                     'gyro_x':msg.gyro_x,
                     'gyro_y':msg.gyro_y,
                     'gyro_z':msg.gyro_z,
                     'mag_x':msg.mag_x,
                     'mag_y':msg.mag_y,
                     'mag_z':msg.mag_z,
                     'quat':msg.quat,
                     'head':msg.head,
                     'depth':'depth',
                     'distance':inches,
                     'switch':switch,
                     'duty':duty
    })
    #print("wrote")

  # battery handling
  if channel == "battery_data":
    msg = battery.decode(data)
    #print("battery   timestamp   = %s" % str(msg.timestamp))
    #print("")
    inches = msg.inches
    switch = msg.switch
    
  # servo handling
  if channel == "servo_data":
    msg = servo.decode(data)
    #print("servo   timestamp   = %s" % str(msg.timestamp))
    #print("")
    duty = msg.duty


# run lcm
lc = lcm.LCM()
lc.subscribe("imu_data", my_handler)
lc.subscribe("battery_data", my_handler)
lc.subscribe("servo_data", my_handler)

try:
  while True:
    lc.handle()
except OSError:
  pass
except KeyboardInterrupt:
  pass
finally:
  print("exiting")
  csvfile.close()