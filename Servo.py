#!/usr/bin/env python3
import time, math

import rcpy
import rcpy.servo as servo
import rcpy.clock as clock

class Servo:

  def __init__(self, channel, duty=0, period=0.02):
    self.channel = channel
    self.duty = duty
    self.period = period

  def angle_to_duty(angle):
    return -1.5 +(3.0/270)(angle+135)

  def set_angle(angle):
    rcpy.set_state(rcpy.RUNNING)

    duty = angle_to_duty(angle)
    srvo.set(duty)

    servo.enable()
    servo.disable()

  def sweep(angle):
    duty = angle_to_duty(angle)

    rcpy.set_state(rcpy.RUNNING)
    clck = clock.Clock(srvo, period)

    try:
      servo.enable()
      clck.start()

      d = 0
      direction = 1
      duty = math.fabs(duty)
      delta = duty/100

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

        time.sleep(.02)

    except KeyboardInterrupt:
        pass

    finally:
        clck.stop()
        servo.disable()
