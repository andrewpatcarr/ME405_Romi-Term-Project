from pyb import Pin, Timer
from time import ticks_us, ticks_diff, ticks_add, ticks_ms

class Motor:
    """
    A class to control a DC motor using PWM and direction signals.

    Attributes
    ----------
    pwm_pin : Pin
        Pin object for the PWM signal controlling motor speed.
    dir_pin : Pin
        Pin object for setting the motor direction.
    slp_pin : Pin
        Pin object for enabling or disabling the motor.
    pwm_timer : Timer
        Timer object configured for PWM signal generation.
    pwm_channel : Timer.channel
        Timer channel used for generating the PWM signal.
    kp : float
        Proportional gain for the PID controller.
    ki : float
        Integral gain for the PID controller.
    integral : float
        Integral term accumulation for the PID controller.
    prev_time : int
        Timestamp of the previous PID update.
    del_time : int
        Time difference between PID updates.
    now : int
        Current timestamp for PID calculations.
    prev_error : float
        Previous error value used in the PID controller.
    """
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
        """
        Moves the motor forward at a specified speed.

        Parameters
        ----------
        speed : int
            Speed percentage (0-100) to apply to the motor.
        """
        self.dir_pin.low()
        self.slp_pin.high()
        self.pwm_channel.pulse_width_percent(speed)

    def reverse(self, speed):
        """
        Moves the motor in reverse at a specified speed.

        Parameters
        ----------
        speed : int
            Speed percentage (0-100) to apply to the motor.
        """
        self.dir_pin.high()
        self.slp_pin.high()
        self.pwm_channel.pulse_width_percent(speed)

    def stop(self):
        """
        Stops the motor by setting PWM to 0 while keeping it enabled.
        """
        self.pwm_channel.pulse_width_percent(0)
        self.slp_pin.high()

    def enable(self):
        """
        Enables the motor by setting sleep pin high while keeping PWM at 0.
        """
        self.pwm_channel.pulse_width_percent(0)
        self.slp_pin.high()

    def disable(self):
        """
        Disables the motor by setting the sleep pin low.
        """
        self.pwm_channel.pulse_width_percent(0)
        self.slp_pin.low()

    def pid(self, des, act, vel, mode):
        """
        Implements a PID controller to adjust motor speed based on error.

        Parameters
        ----------
        des : float
            Desired position or velocity.
        act : float
            Actual measured position or velocity.
        vel : int
            Base velocity adjustment value.
        mode : int
            Control mode (0 for standard PID control, 1 for inverse correction).
        """
        error = des - act
        self.now = ticks_ms()
        self.del_time = ticks_diff(self.now, self.prev_time)
        self.integral += (error - self.prev_error) * (self.del_time / 1000)

        output = int(self.kp * error) + self.ki * self.integral
        if mode == 0:
            if output >= 0:
                self.forward(output)
            elif output < 0:
                self.reverse(-output)
        elif mode == 1:
            if output >= 0:
                self.forward(-output)
            elif output < 0:
                self.reverse(output)

        self.prev_error = error
        self.prev_time = self.now


