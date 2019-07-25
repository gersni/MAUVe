#!/usr/bin/env python3

from datetime import datetime
import rcpy.mpu9250 as mpu9250
import time

import lcm
from exlcm import imu

datetime_format = '%Y%m%d_%H%M%S'

msg = imu()

imu = mpu9250.IMU(enable_dmp=True,
                  dmp_sample_rate=100,
                  enable_magnetometer=True)

lc = lcm.LCM()

start = time.time()

while True:
  if (time.time() - start >= 0):
    imu_out = imu.read()

    #print(imu_out)

    msg.roll = imu_out['tb'][1]
    msg.pitch = imu_out['tb'][0]
    msg.yaw = imu_out['tb'][2]
    msg.accel_x =imu_out['accel'][0]
    msg.accel_y = imu_out['accel'][1]
    msg.accel_z = imu_out['accel'][2]
    msg.gyro_x = imu_out['gyro'][0]
    msg.gyro_y = imu_out['gyro'][1]
    msg.gyro_z = imu_out['gyro'][2]
    msg.mag_x = imu_out['mag'][0]
    msg.mag_y = imu_out['mag'][1]
    msg.mag_z = imu_out['mag'][2]
    msg.quat = str(imu_out['quat'])
    msg.head = imu_out['head']
    msg.timestamp = datetime.strftime(datetime.now(),datetime_format)

    lc.publish("imu", msg.encode())
    start = time.time()
