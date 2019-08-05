#!/usr/bin/env python3

'''
This is a class for controlling the switch
'''

import os
import subprocess

class Switch:

  '''
  Initialize the class, optionally specify which pin is the input signal
  '''
  def __init__(self, pin=97):
    try:
      os.system("echo {pin} > /sys/class/gpio/unexport".format(pin=pin))
    except:
      pass

    os.system("echo {pin} > /sys/class/gpio/export".format(pin=pin))
    os.system("echo in > /sys/class/gpio/gpio{pin}/direction".format(pin=pin))

    self.update_state(self.get_state())

  '''
  Helper function to check the state of the input signal pin and return the int.
  Checking is done by directly reading the file.
  Does not update the object's stored state.
  '''
  def get_state(self):
    #out = subprocess.Popen(["cat", "/sys/class/gpio/gpio97/value"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #stdout,stderr = out.communicate()

    #value = int(stdout)
    f = open("/sys/class/gpio/gpio97/value", "r")

    value = int(f.read())
    
    f.close()

    return value

  '''
  Check if the state has changed and update the object's stored state.
  Returns True is changed or False otherwise.
  '''
  def is_changed_state(self):
    state = self.get_state()
    ret = (state!=self.state)
    self.update_state(state)
    return ret

  '''
  Updates the object state to the state specified in input.
  '''
  def update_state(self, state):
    self.state = state
