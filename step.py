#!/usr/bin/env python3

'''
This program rotates the stepper motor. To change directions, change forward to True or False
'''

from Stepper2 import Stepper2

s = Stepper2()

forward = True

if forward:
  s.step_counterclockwise_infinite(190)
else:
  s.step_clockwise_infinite(190)