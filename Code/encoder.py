import math
from pyb import Timer, Pin
from time import ticks_us, ticks_diff, ticks_add


class Encoder:
    def __init__(self, enc_A_pin, enc_B_pin, enc_timer):
        self.enc_A_pin = Pin(enc_A_pin, mode=Pin.IN)
        self.enc_B_pin = Pin(enc_B_pin, mode=Pin.IN)

        self.timer = Timer(enc_timer, period=0xFFFF, prescaler=0)
        self.timer.channel(1, pin=self.enc_A_pin, mode=Timer.ENC_AB)
        self.timer.channel(2, pin=self.enc_B_pin, mode=Timer.ENC_AB)

        self.encoder_pos = 0
        self.encoder_pos_last = 0
        self.encoder_angle = 0
        self.encoder_velocity = 0
        self.start_time = 0  # [s]
        self.last_time = 0
        self.del_time = 0

        self.current_count = 0
        self.delta = 0
        self.offset = 0

    def update(self, cb_src=None):
        self.start_time = ticks_us()
        self.current_count = self.timer.counter()
        threshold = 0xFFFF
        self.del_time = ticks_diff(self.start_time, self.last_time)
        self.delta = (self.current_count - self.encoder_pos_last - self.offset)

        if self.delta > (threshold + 1)/2:
            self.delta -= (threshold + 1)
            # print('plus')
        elif self.delta < -(threshold + 1)/2:
            self.delta += (threshold + 1)
            # print('minus')
        else:
            pass

        self.encoder_pos_last = self.current_count
        self.encoder_pos += self.delta
        self.encoder_velocity = self.delta/self.del_time  # [rad/s]
        self.last_time = self.start_time

    def zero(self):
        self.encoder_pos = 0
        self.update()

    def get_position(self):
        return self.encoder_pos

    def get_angle(self):
        return self.encoder_angle

    def get_velocity(self):
        return self.encoder_velocity

    def print_enc(self):
        print(self.encoder_pos)