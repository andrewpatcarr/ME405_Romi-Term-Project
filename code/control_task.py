from time import ticks_us, ticks_diff, ticks_add, sleep, time, ticks_ms


class ControlTask:
    def __init__(self, gains, offset):
        self.k_p, self.k_i, self.k_d = gains
        self.offset = offset
        self.S0_init = 0
        self.S1_PID = 1
        self.state = 0
        self.integral = 0.0
        self.derivative = 0.0
        self.now = ticks_ms()
        self.prev_error = 0
        self.left_base = 30
        self.right_base = 30
        self.right_output = 0
        self.left_output = 0
        self.prev_time = 0
        self.del_time = 0

    def controller(self, shares):
        error, right_speed, left_speed = shares
        while True:

            if self.state == self.S0_init:
                self.state = self.S1_PID

                yield self.state

            elif self.state == self.S1_PID:
                error_here = error.get()
                self.now = ticks_ms()
                self.del_time = ticks_diff(self.now,self.prev_time)
                self.integral += error_here*(self.del_time/1000)
                output = (int(self.k_p * error_here) + self.k_i * self.integral)

                # print(f'output control_task: {output}')
                self.prev_error = error_here
                self.prev_time = self.now
                self.right_output = int(self.right_base - output)
                self.left_output = int(self.left_base + output)
                right_speed.put(self.right_output)
                left_speed.put(self.left_output)
                yield self.state
