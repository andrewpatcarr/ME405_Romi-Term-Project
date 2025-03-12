from task_share import Queue
from motor import Motor


class MotorTask:
    """
    A class to control motor speed and movement using PID control.
    
    Attributes
    ----------
    right_motor : Motor
        Motor object for the right motor, controlled using PID.
    left_motor : Motor
        Motor object for the left motor, controlled using PID.
    STOP : int
        State representing a stopped motor (1).
    MOVE : int
        State representing a moving motor (2).
    state : int
        Current state of the motor task (STOP or MOVE).
    current_speed : int
        Current speed setting for the motors.
    """
    def __init__(self, right_motor_pins, left_motor_pins, right_channel, left_channel, r_gains, l_gains):
        """
        Initializes the MotorTask with two motors and their respective control gains.
        
        :param right_motor_pins: Tuple containing pin assignments for the right motor.
        :param left_motor_pins: Tuple containing pin assignments for the left motor.
        :param right_channel: PWM channel for the right motor.
        :param left_channel: PWM channel for the left motor.
        :param r_gains: PID gains for the right motor.
        :param l_gains: PID gains for the left motor.
        """
        self.right_motor = Motor(right_motor_pins, right_channel, r_gains)
        self.left_motor = Motor(left_motor_pins, left_channel, l_gains)

        # Define states
        self.STOP = 1
        self.MOVE = 2

        # Initial state
        self.state = self.STOP
        self.current_speed = 0  # Default speed

    def go(self, shares):
        """
        Controls motor speed and direction based on shared queue values.
        
        :param shares: A tuple containing queues for right/left motor speed, stopping states, and velocity feedback.
        """
        right_speed, left_speed, right_stop, left_stop, right_vel, left_vel = shares

        while True:
            # State execution
            if self.state == self.STOP:
                self.right_motor.stop()
                self.left_motor.stop()
                self.state = self.MOVE
                yield self.state

            elif self.state == self.MOVE:
                # Apply PID control to each motor
                self.right_motor.pid(right_speed.get(), right_vel.get(), 30, 0)
                self.left_motor.pid(left_speed.get(), left_vel.get(), 25, 0)

                yield self.state
