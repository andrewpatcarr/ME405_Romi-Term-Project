import math
from pyb import Timer, Pin
from time import ticks_us, ticks_diff, ticks_add

class Encoder:
    """
    A class to interface with a quadrature encoder using timers.
    
    Attributes
    ----------
    enc_A_pin : Pin
        Pin object for channel A of the encoder.
    enc_B_pin : Pin
        Pin object for channel B of the encoder.
    timer : Timer
        Timer object configured for encoder mode.
    encoder_pos : int
        Accumulated encoder position.
    encoder_pos_last : int
        Previous encoder position.
    encoder_angle : float
        Encoder angle in degrees or radians.
    encoder_velocity : float
        Encoder velocity in counts per second.
    start_time : int
        Timestamp of the last update.
    last_time : int
        Timestamp of the previous update.
    del_time : int
        Time difference between updates.
    current_count : int
        Current raw timer count.
    delta : int
        Difference in encoder counts since last update.
    offset : int
        Offset to correct encoder count.
    """
    
    def __init__(self, enc_A_pin, enc_B_pin, enc_timer):
        """
        Initializes the Encoder with specified pins and timer.
        
        Parameters
        ----------
        enc_A_pin : int
            The pin number for channel A.
        enc_B_pin : int
            The pin number for channel B.
        enc_timer : int
            The timer number for the encoder.
        """
        self.enc_A_pin = Pin(enc_A_pin, mode=Pin.IN)
        self.enc_B_pin = Pin(enc_B_pin, mode=Pin.IN)

        self.timer = Timer(enc_timer, period=0xFFFF, prescaler=0)
        self.timer.channel(1, pin=self.enc_A_pin, mode=Timer.ENC_AB)
        self.timer.channel(2, pin=self.enc_B_pin, mode=Timer.ENC_AB)

        self.encoder_pos = 0
        self.encoder_pos_last = 0
        self.encoder_angle = 0
        self.encoder_velocity = 0
        self.start_time = 0
        self.last_time = 0
        self.del_time = 0

        self.current_count = 0
        self.delta = 0
        self.offset = 0

    def update(self, cb_src=None):
        """
        Updates the encoder position and velocity based on timer counts.
        
        Parameters
        ----------
        cb_src : optional
            Callback source, not used in this implementation.
        """
        self.start_time = ticks_us()
        self.current_count = self.timer.counter()
        threshold = 0xFFFF
        self.del_time = ticks_diff(self.start_time, self.last_time)
        self.delta = (self.current_count - self.encoder_pos_last - self.offset)

        if self.delta > (threshold + 1) / 2:
            self.delta -= (threshold + 1)
        elif self.delta < -(threshold + 1) / 2:
            self.delta += (threshold + 1)

        self.encoder_pos_last = self.current_count
        self.encoder_pos += self.delta
        self.encoder_velocity = self.delta / self.del_time  # [counts/us]
        self.last_time = self.start_time

    def zero(self):
        """Resets the encoder position to zero."""
        self.encoder_pos = 0
        self.update()

    def get_position(self):
        """Returns the current encoder position."""
        return self.encoder_pos

    def get_angle(self):
        """Returns the current encoder angle."""
        return self.encoder_angle

    def get_velocity(self):
        """Returns the current encoder velocity."""
        return self.encoder_velocity

    def print_enc(self):
        """Prints the current encoder position."""
        print(self.encoder_pos)