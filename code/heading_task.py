import time
import cotask
import task_share

class HeadingTask:
    """
    A class to handle reading the heading from an IMU and updating shared variables.

    Attributes
    ----------
    imu : object
        The IMU sensor instance used for reading heading data.
    S0_init : int
        The initialization state value.
    S1_read : int
        The read state value.
    state : int
        The current state value.
    target_heading : int
        The desired target heading value.
    """
    def __init__(self, imu):
        """
        Initializes the HeadingTask object and sets up the IMU sensor.

        Parameters
        ----------
        imu : object
            The IMU sensor instance used to retrieve heading data.
        """
        self.imu = imu

        self.S0_init = 0
        self.S1_read = 1
        self.state = self.S0_init
        self.target_heading = 0


    def get_heading(self, shares):
        """
        The generator that implements the finite state machine for the Heading task.

        State 0 initializes the IMU sensor to heading mode and transitions to state 1. 
        State 1 reads the heading from the IMU, adjusts it within the 0-360° range, 
        and updates the shared variable.

        Parameters
        ----------
        shares : task_share.Share
            A shared variable to store the heading data.

        Yield
        ------
        int
            The value of the current state within the machine.
        """
        heading = shares

        while True:
            if self.state == self.S0_init:
                #print('in init')
                self.imu.set_mode(0x0C)
                self.state = self.S1_read
                yield self.state

            elif self.state == self.S1_read:
                heading_here = (self.imu.read_heading()+90)%360
                #heading_error_here = (self.target_heading - current_heading + 180) % 360 - 180  # Wraparound correction
                #self.error.put(heading_error)
                heading.put(heading_here)
                #print(f'Heading Error: {heading_error_here}')
                yield self.state

