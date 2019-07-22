#!/usr/bin/env python3

from Switch import Switch

s = Switch()

while True:
  if s.is_changed_state():
    print("switch pressed")