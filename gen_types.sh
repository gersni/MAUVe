#!/bin/bash

# This program generates the necessary files to use the 
# imu, battery, and servo LCM channels

lcm-gen -p imu.lcm 
lcm-gen -p battery.lcm
lcm-gen -p servo.lcm
