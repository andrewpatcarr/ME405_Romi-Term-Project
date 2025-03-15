from pyb import Pin, Timer, millis, USB_VCP, UART, ADC, I2C, Switch, ExtInt
from time import ticks_us, ticks_diff, ticks_add, sleep, time, ticks_ms
import math
from motor import Motor
import cotask
import task_share
from encoder_task import EncoderTask
from motor_task import MotorTask
from qtr_sensor import QTRSensor, QTRTask
from control_task import ControlTask
from heading_task import HeadingTask
from BNO055 import BNO055

"""Motor Pin Definitions"""

right_pwm_pin = "B9"
right_dir_pin = "H1"
right_slp_pin = "H0"
right_enc_A = "C7"
right_enc_B = "C6"
right_enc_timer = 8
right_pwm_timer = 4

left_pwm_pin = "B4"
left_dir_pin = "B5"
left_slp_pin = "B6"
left_enc_A = "A0"
left_enc_B = "A1"
left_enc_timer = 2
left_pwm_timer = 3

"""QTR Sensor Pin Definitions"""

ir_1 = 'A6'
ir_3 = 'A7'
ir_5 = 'C2'
ir_7 = 'B0'
ir_9 = 'C4'
ir_11 = 'C3'
ir_13 = 'B1'
ir_ctrl = 'B2'

"""Button Interrupt Creation"""

user_button_pin = 'C13'
button = Pin(user_button_pin, Pin.IN, Pin.PULL_UP)
sw_1 = Switch()
prev_button_state = False
button_state = False


def button_pushed():
    global button_state
    button_state = not button_state
    sleep(.200)  # Debouncing delay


sw_1.callback(button_pushed)


def wait_for_button():
    global button_state, prev_button_state
    while True:
        if button_state != prev_button_state:
            prev_button_state = button_state
            break



enc_pins = [right_enc_A, right_enc_B, right_enc_timer, left_enc_A, left_enc_B, left_enc_timer]
motor_pins = [right_pwm_pin, right_dir_pin, right_slp_pin, right_pwm_timer, left_pwm_pin, left_dir_pin, left_slp_pin,
              left_pwm_timer]
qtr_pins = [ir_1, ir_3, ir_5, ir_7, ir_9, ir_11, ir_13]

"""Create motor objects to stop motors from initial movement."""

right_motor = Motor([right_pwm_pin, right_dir_pin, right_slp_pin, right_pwm_timer], 4, [1, 0])
left_motor = Motor([left_pwm_pin, left_dir_pin, left_slp_pin, left_pwm_timer], 1, [1, 0])
right_motor.stop()
left_motor.stop()

"""Initialize i2c3"""

i2c = I2C(3, I2C.CONTROLLER)  # Make sure you're using the correct I2C bus
sleep(1)  # Allow devices to power up

"""Bumper Interrupt Creation"""

bumper_pin = Pin('B14', Pin.IN, Pin.PULL_UP)
prev_bumper_state = False
bumper_state = False
last_interrupt_time = 0  # Stores the last trigger time
debounce_delay = 50  # Debounce delay in milliseconds


def bumper_pushed(line):
    global bumper_state, last_interrupt_time
    current_time = millis()  # Get current time in ms
    if (current_time - last_interrupt_time) > debounce_delay:  # Check debounce
        bumper_state = True
        last_interrupt_time = current_time  # Update last trigger time


bumper_inter = ExtInt(bumper_pin, ExtInt.IRQ_FALLING, Pin.PULL_UP, bumper_pushed)

"""Create Sensor and Task Objects"""

encoder = EncoderTask(enc_pins)
motor = MotorTask(motor_pins[0:4], motor_pins[4:8], 4, 1, [.7, 0], [.9, 0])
qtr = QTRSensor(qtr_pins, ir_ctrl)
qtr_more = QTRTask(qtr)
control = ControlTask([18, 0, 0], 0)  # [k_p, k_i, K_d], offset
imu = BNO055(i2c, 'A15')
imu_more = HeadingTask(imu)

if __name__ == '__main__':
    """Create shares"""
    right_pos = task_share.Share('f', name='Right Encoder Pos')
    left_pos = task_share.Share('f', name='Left Encoder Pos')
    right_vel = task_share.Share('f', name='Right Encoder Vel')
    left_vel = task_share.Share('f', name='Left Encoder Vel')
    right_speed = task_share.Share('h', name="Right Speed")  # Input Speed for motor pwm [%]
    right_stop = task_share.Share('h', name="Right Stop")
    left_speed = task_share.Share('h', name="Left speed")  # Input Speed for motor pwm [%]
    left_stop = task_share.Share('h', name="Left Stop")
    line_error = task_share.Share('f', name="Error")
    heading = task_share.Share('f', name="Heading")
    line_heading = task_share.Share('h', name="Line Switch")
    heading_set = task_share.Share('f', name="Heading Set")

    """Create Tasks"""
    enc_task = cotask.Task(encoder.encoder_gen, name='Encoder Task', priority=1, period=1,
                           shares=([right_pos, right_vel, left_pos, left_vel]), trace=False, profile=True)

    motor_task = cotask.Task(motor.go, name='Motor Task', priority=1, period=8,
                             shares=([right_speed, left_speed, right_stop, left_stop, right_vel, left_vel]),
                             trace=False, profile=True)
    controller_task = cotask.Task(control.controller, name='Control Task', priority=1, period=8,
                                  shares=[line_error, right_speed, left_speed, line_heading, heading, heading_set],
                                  trace=False, profile=True)
    qtr_task = cotask.Task(qtr_more.get_line, name='QTR Task', priority=1, period=10, shares=line_error, trace=False,
                           profile=True)
    imu_task = cotask.Task(imu_more.get_heading, name='IMU Task', priority=1, period=15, shares=heading, trace=False,
                           profile=True)

    """Add Tasks to cotask task list"""
    cotask.task_list.append(enc_task)
    cotask.task_list.append(qtr_task)
    cotask.task_list.append(controller_task)
    cotask.task_list.append(motor_task)
    cotask.task_list.append(imu_task)

    """Put motor in stopped mode"""
    right_speed.put(0)
    right_stop.put(1)
    left_speed.put(0)
    left_stop.put(1)

    """Calibration (if needed)"""
    # print('place on white')
    # wait_for_button()
    # qtr.calibrate_white()
    #
    # print('place on black')
    # wait_for_button()
    # qtr.calibrate_black()

    """Print timing initialization"""
    interval = 500
    begin_time = ticks_ms()
    deadline = ticks_add(begin_time, interval)

    """Take motors out of stop mode"""
    right_stop.put(0)
    left_stop.put(0)

    """Course State Machine Definitions"""
    state = 0
    S0_wait_to_start = 0
    S1_to_diamond = 1
    S2_straightline_diamond = 2
    S3_to_grid = 3
    S4_to_turn = 4
    S5_turn_1 = 5
    S6_to_wall = 6
    S7_reverse = 7
    S8_turn_2 = 8
    S9_to_3 = 9
    S10_turn_3 = 10
    S11_to_4 = 11
    S12_turn_4 = 12
    S13_to_finish = 13

    thresh = 0
    rep = 0
    heading_north = 0
    hed_set = 0

    print('Press button to start run')

    try:
        while True:
            cotask.task_list.pri_sched()
            """Print Section"""
            now = ticks_ms()
            if ticks_diff(deadline, now) < 0:
                print(
                    f'Right_Pos- thresh: {right_pos.get() - thresh}, State: {state}, R_speed: {right_speed.get()}, Heading: {heading.get()}')
                deadline = ticks_add(deadline, interval)

            """Course State machine
            
            Hardcoded states based on encoder position and bumper state.
            Jumps between line sensing and north sensing modes to complete the course.
            """

            if state == S0_wait_to_start:
                line_heading.put(4)
                if button_state != prev_button_state:
                    prev_button_state = button_state
                    sleep(.2)
                    state = S1_to_diamond
            elif button_state != prev_button_state:
                prev_button_state = button_state
                state = S0_wait_to_start

            if state == S1_to_diamond:
                line_heading.put(0)
                if rep == 0:
                    thresh = right_pos.get() + 5_500
                    heading_north = (imu.read_heading()+90)%360
                    print(f'Heading North: {heading_north}')
                    rep += 1

                if right_pos.get() > thresh:
                    state = S2_straightline_diamond
                    rep = 0

            if state == S2_straightline_diamond:

                if rep == 0:
                    line_heading.put(1)
                    hed_set = heading_north + 90

                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    heading_set.put(hed_set)
                    thresh = right_pos.get() + 1_000
                    print(f'Threshold: {thresh}, hed_set: {hed_set}')
                    rep += 1
                if right_pos.get() > thresh:
                    state = S3_to_grid
                    rep = 0
            if state == S3_to_grid:
                line_heading.put(0)
                if rep == 0:
                    thresh = right_pos.get() + 16_000
                    rep += 1
                if right_pos.get() > thresh:
                    state = S4_to_turn
                    rep = 0
            if state == S4_to_turn:
                line_heading.put(1)
                if rep == 0:
                    thresh = right_pos.get() + 4_000
                    hed_set = heading_north - 180
                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    heading_set.put(hed_set)
                    rep += 1
                if right_pos.get() > thresh:
                    state = S5_turn_1
                    right_speed.put(0)
                    left_speed.put(0)
                    rep = 0
            if state == S5_turn_1:
                if rep == 0:
                    hed_set = heading_north - 90
                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    heading_set.put(hed_set)
                    line_heading.put(2)
                    rep += 1
                if -10 < (hed_set - heading.get()) < 10:
                    right_speed.put(0)
                    left_speed.put(0)
                    state = S6_to_wall
                    rep = 0
            if state == S6_to_wall:
                line_heading.put(0)
                if bumper_state:
                    print(f'Bumper hit')
                    right_speed.put(0)
                    left_speed.put(0)
                    state = S7_reverse
            if state == S7_reverse:
                line_heading.put(3)

                if rep == 0:
                    thresh = right_pos.get() - 500
                    hed_set = heading_north - 90

                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    print(f'hed_set: {hed_set}')
                    heading_set.put(hed_set)
                    rep += 1
                if right_pos.get() < thresh:
                    right_speed.put(0)
                    left_speed.put(0)
                    state = S8_turn_2
                    rep = 0
            if state == S8_turn_2:
                line_heading.put(2)
                if rep == 0:
                    hed_set = heading_north
                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    heading_set.put(hed_set)
                    line_heading.put(2)
                    rep += 1
                if -10 < (hed_set - heading.get()) < 10:
                    right_speed.put(0)
                    left_speed.put(0)
                    state = S9_to_3
                    rep = 0
            if state == S9_to_3:
                line_heading.put(1)
                heading_set.put(heading_north)
                if rep == 0:
                    thresh = right_pos.get() + 2_000
                    rep += 1
                if right_pos.get() > thresh:
                    state = S10_turn_3
                    rep = 0
            if state == S10_turn_3:
                line_heading.put(2)
                if rep == 0:
                    hed_set = heading_north - 90
                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    heading_set.put(hed_set)
                    line_heading.put(2)
                    rep += 1
                if -10 < (hed_set - heading.get()) < 10:
                    right_speed.put(0)
                    left_speed.put(0)
                    state = S11_to_4
                    rep = 0
            if state == S11_to_4:
                line_heading.put(1)
                hed_set = heading_north - 90
                if hed_set < 0:
                    hed_set += 360
                elif hed_set > 360:
                    hed_set -= 360
                heading_set.put(hed_set)
                if rep == 0:
                    thresh = right_pos.get() + 2_000
                    rep += 1
                if right_pos.get() > thresh:
                    state = S12_turn_4
                    rep = 0
            if state == S12_turn_4:
                line_heading.put(2)
                if rep == 0:
                    hed_set = heading_north - 180
                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    heading_set.put(hed_set)
                    line_heading.put(2)
                    rep += 1
                if -10 < (hed_set - heading.get()) < 10:
                    right_speed.put(0)
                    left_speed.put(0)
                    state = S13_to_finish
                    rep = 0
            if state == S13_to_finish:
                if rep == 0:
                    hed_set = heading_north - 180
                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    heading_set.put(hed_set)
                    line_heading.put(1)
                    thresh = right_pos.get() + 2_200
                    rep += 1
                if right_pos.get() > thresh:
                    state = S0_wait_to_start
                    rep = 0

                    print('Done!')


    except KeyboardInterrupt:
        print('done hopefully')
    right_speed.put(0)
    right_stop.put(1)
    left_speed.put(0)
    left_stop.put(1)
    # print('\n' + str(cotask.task_list))
    # print(task_share.show_all())
    # print('')
    while True:
        cotask.task_list.pri_sched()
        pass



