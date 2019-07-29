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

  def angle_to_duty(self, angle):
    return -1.5 +(3.0/270)*(angle+135)

  def set_angle(self, angle):
    rcpy.set_state(rcpy.RUNNING)
    srvo = servo.Servo(self.channel)
    
    duty = self.angle_to_duty(angle)
    print(duty)
    srvo.set(duty)
    
    clck = clock.Clock(srvo, self.period)

    servo.enable()
    clck.start()
    clck.stop()
    servo.disable()

  def sweep(self, angle):
    rcpy.set_state(rcpy.RUNNING)
    srvo = servo.Servo(self.channel)
    
    duty = self.angle_to_duty(angle)
    
    clck = clock.Clock(srvo, self.period)

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
