#!/usr/bin/env python3
import time, math

from datetime import datetime

import rcpy
import rcpy.servo as servo
import rcpy.clock as clock

import lcm
from exlcm import servo as servolcm

datetime_format = '%Y%m%d_%H%M%S'

class Servo:

  def __init__(self, channel, period=0.02):
    self.channel = channel
    self.period = period
    
    self.lc = lcm.LCM()

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
    
    self.duty = duty
    
    msg = servolcm()
    msg.duty = self.duty
    msg.timestamp = datetime.strftime(datetime.now(),datetime_format)

    self.lc.publish("servo_data", msg.encode())

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
        self.duty = d
        
        msg = servolcm()
        msg.duty = self.duty
        msg.timestamp = datetime.strftime(datetime.now(),datetime_format)

        self.lc.publish("servo_data", msg.encode())

        time.sleep(.02)

    except KeyboardInterrupt:
        pass

    finally:
        clck.stop()
        servo.disable()
