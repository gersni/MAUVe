#!/usr/bin/env python3

'''
This program tests whether the switch is working by continuously checking the state,
and printing a message when it detects a switch change
'''

from Switch import Switch

s = Switch()

while True:
  if s.is_changed_state():
    print("switch pressed")