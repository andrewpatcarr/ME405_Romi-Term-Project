import time
import cotask
import task_share

class HeadingTask:

    def __init__(self, imu):

        self.imu = imu

        self.S0_init = 0
        self.S1_read = 1
        self.state = self.S0_init
        self.target_heading = 0


    def get_heading(self, shares):

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

