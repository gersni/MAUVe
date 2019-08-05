#!/usr/bin/env python3

'''
This program runs the servo, sweeping it from -a to +a degrees
'''

from Servo import Servo

a = 135

s = Servo(8)

s.sweep(a)