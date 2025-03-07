from encoder import Encoder

class EncoderTask:
    def __init__(self, pins):
        right_enc_A = pins[0]
        right_enc_B = pins[1]
        right_enc_timer = pins[2]
        left_enc_A = pins[3]
        left_enc_B = pins[4]
        left_enc_timer = pins[5]
        self.S0_init = 0
        self.S1_read = 1

        self.state = self.S0_init

        self.right_encoder = Encoder(right_enc_A, right_enc_B, right_enc_timer)
        self.left_encoder = Encoder(left_enc_A, left_enc_B, left_enc_timer)

    def encoder_gen(self, shares):

        # implement finite state machine
        right_pos, right_vel, left_pos, left_vel = shares
        while True:
            # print('in encoder task')
            if self.state == self.S0_init:
                self.right_encoder.zero()  # Reset right encoder
                self.left_encoder.zero()   # Reset left encoder
                self.state = self.S1_read
                yield self.S1_read

            if self.state == self.S1_read:
                self.right_encoder.update()
                self.left_encoder.update()
                # Read right encoder
                right_pos.put(self.right_encoder.get_position())
                right_vel.put(self.right_encoder.get_velocity())
                # Read left encoder
                left_pos.put(self.left_encoder.get_position())
                left_vel.put(self.left_encoder.get_velocity())
                # print(f'Right Pos: {right_pos.get()}')
                yield self.S1_read


"""
from encoder import Encoder
from pyb import Pin, Timer, millis
from time import ticks_us, ticks_diff, ticks_add, sleep, time, ticks_ms
class EncoderTask:
    def __init__(self, pins):
        right_enc_A = pins[0]
        right_enc_B = pins[1]
        right_enc_timer = pins[2]
        left_enc_A = pins[3]
        left_enc_B = pins[4]
        left_enc_timer = pins[5]

        self.S0_init = 0
        self.S1_read = 1
        self.state = self.S0_init

        self.right_encoder = Encoder(right_enc_A, right_enc_B, right_enc_timer)
        self.left_encoder = Encoder(left_enc_A, left_enc_B, left_enc_timer)

        # Averaging Variables
        self.n = 0  # Counter for averaging
        self.right_position_total = 0
        self.right_velocity_total = 0
        self.left_position_total = 0
        self.left_velocity_total = 0

        # Print CSV header
        print("Timestamp,Right Position,Right Velocity,Left Position,Left Velocity,")

    def encoder_gen(self, shares):
        right_pos, right_vel, left_pos, left_vel = shares

        while True:
            if self.state == self.S0_init:
                self.right_encoder.zero()  # Reset right encoder
                self.left_encoder.zero()   # Reset left encoder
                self.state = self.S1_read
                yield 1

            if self.state == self.S1_read:
                self.right_encoder.update()
                self.left_encoder.update()

                # Accumulate position and velocity values for averaging
                self.right_position_total += self.right_encoder.get_position()
                self.right_velocity_total += self.right_encoder.get_velocity()
                self.left_position_total += self.left_encoder.get_position()
                self.left_velocity_total += self.left_encoder.get_velocity()

                self.n += 1  # Increase counter

                # Compute average every `n` cycles
                if self.n > 5:  # Adjust the number of cycles as needed
                    avg_right_pos = self.right_position_total / self.n
                    avg_right_vel = self.right_velocity_total / self.n
                    avg_left_pos = self.left_position_total / self.n
                    avg_left_vel = self.left_velocity_total / self.n

                    right_pos.put(avg_right_pos)
                    right_vel.put(avg_right_vel)
                    left_pos.put(avg_left_pos)
                    left_vel.put(avg_left_vel)

                    # Print CSV-style data
                    timestamp = millis()  # Time in milliseconds
                    print(f"{timestamp},{avg_right_pos},{avg_right_vel},{avg_left_pos},{avg_left_vel},")

                    # Reset totals and counter
                    self.right_position_total = 0
                    self.right_velocity_total = 0
                    self.left_position_total = 0
                    self.left_velocity_total = 0
                    self.n = 0

                yield 1
"""


"""
from encoder import Encoder
from pyb import Pin, Timer, millis
from time import ticks_us, ticks_diff, ticks_add, sleep, time, ticks_ms

class EncoderTask:
    def __init__(self, pins):
        right_enc_A = pins[0]
        right_enc_B = pins[1]
        right_enc_timer = pins[2]
        left_enc_A = pins[3]
        left_enc_B = pins[4]
        left_enc_timer = pins[5]

        self.S0_init = 0
        self.S1_read = 1
        self.state = self.S0_init

        self.right_encoder = Encoder(right_enc_A, right_enc_B, right_enc_timer)
        self.left_encoder = Encoder(left_enc_A, left_enc_B, left_enc_timer)

        # Timing Variables
        self.interval = 5_000  # Interval in microseconds
        self.start_time = ticks_us()  # Start time
        self.deadline = ticks_add(self.start_time, self.interval)

        # Averaging Variables
        self.n = 0  # Counter for averaging
        self.right_position_total = 0
        self.right_velocity_total = 0
        self.left_position_total = 0
        self.left_velocity_total = 0

        # Print CSV Header
        print("Time (ms),Position,Velocity,")
    def encoder_gen(self, shares):
        start_time = 0
        time_elapsed = 0
        right_pos, right_vel, left_pos, left_vel, rolling = shares
        start_time = millis()
        
        while True:
            now = ticks_us()

            if ticks_diff(self.deadline, now) < 0:
                self.right_encoder.update()
                self.left_encoder.update()

                # Compute elapsed time
                time_elapsed = millis() - start_time -110

                # Accumulate position and velocity values for averaging
                self.right_position_total += self.right_encoder.get_position()
                self.right_velocity_total += self.right_encoder.get_velocity()
                self.left_position_total += self.left_encoder.get_position()
                self.left_velocity_total += self.left_encoder.get_velocity()
                self.n += 1  # Increase counter
                #print(f"{time_elapsed},{self.right_encoder.get_position()},{self.right_encoder.get_velocity()},")
                # Compute average every `n` cycles
                if self.n > 5:  # Adjust for smoother data
                    avg_right_pos = self.right_position_total / self.n
                    avg_right_vel = self.right_velocity_total / self.n
                    avg_left_pos = self.left_position_total / self.n
                    avg_left_vel = self.left_velocity_total / self.n

                    right_pos.put(avg_right_pos)
                    right_vel.put(avg_right_vel)
                    left_pos.put(avg_left_pos)
                    left_vel.put(avg_left_vel)

                    # Print CSV-friendly output
                    if 0 < time_elapsed < 1100 :
                        print(f"{time_elapsed},{avg_left_pos},{avg_left_vel},")
                    #{avg_right_pos},{avg_right_vel},
                    #{avg_left_pos},{avg_left_vel}
                    # Reset totals and counter
                    self.right_position_total = 0
                    self.right_velocity_total = 0
                    self.left_position_total = 0
                    self.left_velocity_total = 0
                    self.n = 0

                # Update deadline for next cycle
                self.deadline = ticks_add(self.deadline, self.interval)

                # Stop condition (Optional)
                if time_elapsed > 1000:
                    rolling.put(0)
                    #print("Stopping encoder")
                    

            yield 1

"""
