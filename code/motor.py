from pyb import Pin, Timer

class Motor:
    def __init__(self, pins, pwm_channel):
        self.pwm_pin = Pin(pins[0], mode=Pin.OUT_PP)
        self.dir_pin = Pin(pins[1], mode=Pin.OUT_PP)
        self.slp_pin = Pin(pins[2], mode=Pin.OUT_PP)

        self.pwm_timer = Timer(pins[3], freq=22000, prescaler=0)
        self.pwm_channel = self.pwm_timer.channel(pwm_channel, Timer.PWM, pin=self.pwm_pin)

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

