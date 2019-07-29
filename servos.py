#!/usr/bin/env python3
import time, math

import rcpy
import rcpy.servo as servo
import rcpy.clock as clock

channel = 8
duty = 1.0
sweep = False
period = 0.02

# set state to rcpy.RUNNING
rcpy.set_state(rcpy.RUNNING)

# set servo duty (only one option at a time)
srvo = servo.Servo(channel)

if duty != 0:
  if not sweep:
    srvo.set(duty)
else:
  sweep = False


clck = clock.Clock(srvo, period)

# enable servos
servo.enable()

# start clock
clck.start()

'''
# sweep
if sweep:

  d = 0
  direction = 1
  duty = math.fabs(duty)
  delta = duty/100

  # keep running
  while rcpy.get_state() != rcpy.EXITING:

    # increment duty
    d = d + direction * delta

    # end of range?
    if d > duty or d < -duty:
      direction = direction * -1
      if d > duty:
        d = duty
      else:
        d = -duty

    srvo.set(d)

    # sleep some
    time.sleep(.02)

'''

clck.stop()
servo.disable()




