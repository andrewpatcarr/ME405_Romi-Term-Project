import time
import cotask
import task_share

class HeadingTask:

    def __init__(self, imu, right_speed, left_speed, error, Kp=1.5):

        self.imu = imu
        self.right_speed = right_speed
        self.left_speed = left_speed
        self.error = error
        self.Kp = Kp
        self.target_heading = 0  # North

    def adjust_heading(self):

        while True:
            current_heading = self.imu.read_heading()
            heading_error = (self.target_heading - current_heading + 180) % 360 - 180  # Wraparound correction
            self.error.put(heading_error)

            # Apply proportional control
            turn_speed = int(self.Kp * heading_error)
            turn_speed = max(min(turn_speed, 40), -40)  # Limit speed range

            if abs(heading_error) > 2:  # Avoid unnecessary small adjustments
                self.right_speed.put(-turn_speed)
                self.left_speed.put(turn_speed)
            else:
                self.right_speed.put(0)
                self.left_speed.put(0)

            yield  # Allow cooperative multitasking

