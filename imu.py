#!/usr/bin/env python3

'''
This program runs the imu and prints the output.
'''

import rcpy.mpu9250 as mpu9250

imu = mpu9250.IMU(enable_dmp = True, dmp_sample_rate = 4,
                  enable_magnetometer = True)

print(imu.read())
