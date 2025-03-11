from pyb import Pin, Timer
from time import ticks_us, ticks_diff, ticks_add, ticks_ms

class Motor:
    def __init__(self, pins, pwm_channel, gains):
        self.pwm_pin = Pin(pins[0], mode=Pin.OUT_PP)
        self.dir_pin = Pin(pins[1], mode=Pin.OUT_PP)
        self.slp_pin = Pin(pins[2], mode=Pin.OUT_PP)

        self.pwm_timer = Timer(pins[3], freq=22000, prescaler=0)
        self.pwm_channel = self.pwm_timer.channel(pwm_channel, Timer.PWM, pin=self.pwm_pin)

        self.kp, self.ki = gains
        self.integral = 0
        self.prev_time = ticks_ms()
        self.del_time = 0
        self.now = ticks_ms()
        self.prev_error = 0



    def forward(self, speed):
        self.dir_pin.low()
        self.slp_pin.high()
        self.pwm_channel.pulse_width_percent(speed)

    def reverse(self, speed):
        self.dir_pin.high()
        self.slp_pin.high()
        self.pwm_channel.pulse_width_percent(speed)

    def stop(self):
        self.pwm_channel.pulse_width_percent(0)
        self.slp_pin.high()

    def enable(self):
        self.pwm_channel.pulse_width_percent(0)
        self.slp_pin.high()

    def disable(self):
        self.pwm_channel.pulse_width_percent(0)
        self.slp_pin.low()

    def pid(self, des, act, vel, mode):
        error = des - act
        self.now = ticks_ms()
        self.del_time = ticks_diff(self.now, self.prev_time)
        self.integral += (error-self.prev_error) * (self.del_time / 1000)

        output = int(self.kp * error) + self.ki * self.integral

        if mode == 0:
            self.forward(output + vel)
        elif mode == 1:
            if output >= 0:
                self.forward(-output)
            elif output < 0:
                self.reverse(output)

        self.prev_error = error
        self.prev_time = self.now



