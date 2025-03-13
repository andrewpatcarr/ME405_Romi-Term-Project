from time import ticks_us, ticks_diff, ticks_add, sleep, time, ticks_ms

class ControlTask:
    """
    A class to implement a PID controller for motor speed adjustments.

    Attributes
    ----------
    k_p : float
        Proportional gain.
    k_i : float
        Integral gain.
    k_d : float
        Derivative gain (not used in this version).
    offset : int
        Offset value for control adjustments.
    integral : float
        Accumulated integral term for PID control.
    prev_error : float
        Previous error value for integral calculation.
    now : int
        Current timestamp (milliseconds).
    prev_time : int
        Previous timestamp (milliseconds).
    del_time : int
        Time difference between control updates.
    left_base : int
        Base speed for left motor.
    right_base : int
        Base speed for right motor.
    left_output : int
        Output speed for left motor.
    right_output : int
        Output speed for right motor.
    """
    
    def __init__(self, gains, offset):
        """
        Initializes the PID controller with given gains and offsets.

        Parameters
        ----------
        gains : tuple[float, float, float]
            (k_p, k_i, k_d) gains for PID control.
        offset : int
            Speed offset for base control.
        """
        self.k_p, self.k_i, self.k_d = gains  # Assign PID gains
        self.offset = offset  # Assign offset value

        # Define FSM states
        self.S0_init = 0
        self.S1_PID = 1
        self.state = self.S0_init  # Start in initialization state

        # Initialize PID variables
        self.integral = 0.0
        self.derivative = 0.0
        self.prev_error = 0
        self.prev_time = 0
        self.del_time = 0
        self.now = ticks_ms()

        # Base speed values for motors
        self.base_speed = 35
        self.speed = 0
        self.left_output = 0
        self.right_output = 0
        self.stepper = 0
        self.heading_set = 0

    def controller(self, shares):
        """
        Implements the PID control loop.

        State 0: Initializes the system and moves to PID state.
        State 1: Reads the error, applies PID corrections, and updates motor speeds.

        Parameters
        ----------
        shares : list[SharedVariable]
            Shared variables for error, right motor speed, and left motor speed.

        Yields
        ------
        state : int
            The current FSM state.
        """
        line_error, right_speed, left_speed, line_heading, heading, heading_set = shares
        while True:
            error_here = 0
            if self.state == self.S0_init:
                self.state = self.S1_PID
                yield self.state

            elif self.state == self.S1_PID:
                line_heading_here = line_heading.get()
                if line_heading_here == 0:
                    error_here = line_error.get()
                    self.speed = self.base_speed

                    self.now = ticks_ms()
                    self.del_time = ticks_diff(self.now, self.prev_time)

                    self.integral += error_here * (self.del_time / 1000)

                    output = int(self.k_p * error_here + self.k_i * self.integral)

                    self.prev_error = error_here
                    self.prev_time = self.now

                    right_speed.put(int(self.speed - output))
                    left_speed.put(int(self.speed + output))

                    yield self.state
                elif line_heading_here == 1 or line_heading_here == -1:
                    if line_heading_here == 1:
                        self.speed = self.base_speed
                    else:
                        self.speed = -self.base_speed

                    error_here = heading.get() - heading_set.get()
                    self.now = ticks_ms()
                    self.del_time = ticks_diff(self.now, self.prev_time)

                    self.integral += error_here * (self.del_time / 1000)

                    output = int((self.k_p/25) * error_here + self.k_i * self.integral)

                    self.prev_error = error_here
                    self.prev_time = self.now

                    # right_speed.put(int(self.speed + line_heading_here*output))
                    # left_speed.put(int(self.speed - line_heading_here*output))
                    right_speed.put(max(-60, min(int(self.speed + line_heading_here*output), 60)))
                    left_speed.put(max(-60, min(int(self.speed - line_heading_here*output), 60)))

                    yield self.state
                elif line_heading_here == 2:  # turn state
                    error_here = heading.get() - heading_set.get()
                    self.now = ticks_ms()
                    self.del_time = ticks_diff(self.now, self.prev_time)

                    self.integral += error_here * (self.del_time / 1000)

                    output = int((15/25) * error_here + self.k_i * self.integral)

                    self.prev_error = error_here
                    self.prev_time = self.now

                    right_speed.put(max(-60, min(output, 60)))
                    left_speed.put(max(-60, min(-output, 60)))

                    yield self.state
                elif line_heading_here == 3:
                    self.right_output = -30
                    self.left_output = -30
                    right_speed.put(self.right_output)
                    left_speed.put(self.left_output)
                    yield self.state
                elif line_heading_here == 4:
                    self.right_output = 0
                    self.left_output = 0
                    right_speed.put(self.right_output)
                    left_speed.put(self.left_output)
                    yield self.state
