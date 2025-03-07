from time import ticks_us, ticks_diff, ticks_add, sleep, time, ticks_ms
from pyb import millis

class DataCollectionTask:
    def __init__(self):
        self.interval = 5_000
        self.start = ticks_us()
        self.deadline = ticks_add(self.start, self.interval)

        self.S0_init = 0
        self.S1_ready = 1
        self.S2_step_right = 2
        self.S3_step_left = 3
        self.S4_print = 4
        self.state = 0

        self.begin = 0
        self.n = 0
        self.now = ticks_us()
        self.start_time = ticks_ms
        self.time_elapsed = 0


    def collect(self, shares):
        (right_pos, right_vel, left_pos, left_vel, right_mes_pos,
         left_mes_pos, right_mes_vel, left_mes_vel, times, data_collect, rolling) = shares
        right_positionTotal = 0
        right_velocityTotal = 0
        left_positionTotal = 0
        left_velocityTotal = 0
        time_elapsedTotal = 0
        start_time = 0
        while True:

            if self.state == self.S0_init:
                print('in data collection s0')
                self.start = ticks_us()
                self.deadline = ticks_add(self.start, self.interval)
                self.state = self.S1_ready
                yield self.state
            elif self.state == self.S1_ready:
                print('in data collection s1')
                self.deadline = ticks_add(self.deadline, self.interval)
                if data_collect.get() == 0:
                    yield self.state
                elif data_collect.get() == 1:
                    self.state = self.S2_step_right
                    yield self.state
            elif self.state == self.S2_step_right:
                #print('in data collection s2')
                if self.begin == 0:
                    self.begin = 1
                    print('begin happened')
                    self.start = ticks_us()
                    self.deadline = ticks_add(self.start, self.interval)
                    rolling.put(1)
                    self.start_time = millis()
                    self.n = 0


                self.now = ticks_us()

                if ticks_diff(self.deadline, self.now) < 0:
                    current_time = millis()
                    self.time_elapsed = current_time - self.start_time

                    right_positionTotal += right_pos.get()
                    right_velocityTotal += right_vel.get()
                    left_positionTotal += left_pos.get()
                    left_velocityTotal += left_vel.get()
                    self.n += 1
                    if self.n > 0:
                        right_position = right_positionTotal / self.n
                        right_velocity = right_velocityTotal / self.n
                        left_position = left_positionTotal / self.n
                        left_velocity = left_velocityTotal / self.n
                        #print(f'Position, {right_position}')
                        #print(f'Velocity, {right_velocity}')
                        #time_elapsed = time_elapsedTotal / n
                        right_mes_pos.put(right_position)
                        left_mes_pos.put(left_position)
                        right_mes_vel.put(right_velocity)
                        left_mes_vel.put(left_velocity)
                        times.put(self.time_elapsed)
                        self.right_positionTotal = 0
                        self.right_velocityTotal = 0
                        self.left_positionTotal = 0
                        self.left_velocityTotal = 0
                        self.n = 0

                    self.deadline = ticks_add(self.deadline, self.interval)
                    #print(f'time {self.time_elapsed}')
                    if self.time_elapsed > 1500:
                        rolling.put(0)
                        self.state = self.S4_print
                        yield self.state
                    else:
                        yield self.state
            elif self.state == self.S3_step_left:
                yield self.state
            elif self.state == self.S4_print:
                #if right_mes_vel.get() !=0:
                    #print(f'Velocity, {right_mes_vel.get()}')
                    #print(f'Position, {right_mes_pos.get()}')
                    #print(f'{times.get()},{right_mes_pos.get()},{right_mes_vel.get()},')
                if right_mes_vel.get() >0:
                    #print(f'{times.get()},{right_mes_pos.get()},{right_mes_vel.get()},')
                    yield self.state
                elif left_mes_vel.get()>0:
                    #print(f'{times.get()},{left_mes_pos.get()},{left_mes_vel.get()},')
                    yield self.state
                else:
                    self.state = self.S1_ready
                    #print("DCT Going to state 1")
                    yield self.state


