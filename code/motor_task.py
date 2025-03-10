from task_share import Queue
from motor import Motor
import time


class MotorTask:
    def __init__(self, right_motor_pins, left_motor_pins, right_channel, left_channel):
        """
        Initializes the MotorTask.
        """
        self.right_motor = Motor(right_motor_pins, right_channel)
        self.left_motor = Motor(left_motor_pins, left_channel)

        # Define states
        self.STOP = 1
        self.MOVE = 2

        # Initial state
        self.state = self.STOP
        self.current_speed = 0  # Default speed

    def go(self, shares):
        #  speed positive means forward, speed negative means reverse
        # stop = 0 means not stopped, 1 means stopped and hold, 2 means coast
        right_speed, left_speed, right_stop, left_stop = shares

        while True:
            # State execution
            if self.state == self.STOP:
                self.right_motor.stop()
                self.left_motor.stop()
                self.state = self.MOVE
                yield self.state

            elif self.state == self.MOVE:
                if right_speed.get() > 0 and right_stop.get() == 0:
                    self.right_motor.forward(right_speed.get())
                elif right_speed.get() < 0 and right_stop.get() == 0:
                    self.right_motor.reverse(right_speed.get())
                else:
                    self.right_motor.stop()

                if left_speed.get() > 0 and left_stop.get() == 0:
                    self.left_motor.forward(left_speed.get())
                elif left_speed.get() < 0 and left_stop.get() == 0:
                    self.left_motor.reverse(left_speed.get())
                else:
                    self.left_motor.stop()
                # print(f'Right Speed: {right_speed.get()}, Left Speed: {left_speed.get()}')
                yield self.state
