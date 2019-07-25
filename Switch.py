#!/usr/bin/env python3

import os
import subprocess

class Switch:

  def __init__(self, pin=97):
    try:
      os.system("echo {pin} > /sys/class/gpio/unexport".format(pin=pin))
    except:
      pass

    os.system("echo {pin} > /sys/class/gpio/export".format(pin=pin))
    os.system("echo in > /sys/class/gpio/gpio{pin}/direction".format(pin=pin))

    self.update_state(self.get_state())

  def get_state(self):
    #out = subprocess.Popen(["cat", "/sys/class/gpio/gpio97/value"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #stdout,stderr = out.communicate()

    #value = int(stdout)
    f = open("/sys/class/gpio/gpio97/value", "r")

    value = int(f.read())

    return value

  def is_changed_state(self):
    state = self.get_state()
    ret = (state!=self.state)
    self.update_state(state)
    return ret

  def update_state(self, state):
    self.state = state
