from pyb import Pin, Timer, millis, USB_VCP, UART, ADC, I2C
from time import ticks_us, ticks_diff, ticks_add, sleep, time, ticks_ms
import math
from motor import Motor
import cotask
import task_share
from encoder_task import EncoderTask
from motor_task import MotorTask
from data_collection_task import DataCollectionTask
from qtr_sensor import QTRSensor, QTRTask
from control_task import ControlTask
from heading_task import HeadingTask
from BNO055 import BNO055
#from user_task import User

# Make a serial port object from the UART class
BT_ser = UART(5, 115200)

# Deconfigure default pins
Pin('B6',  mode=Pin.ANALOG)     # Set pin modes back to default
Pin('B7',  mode=Pin.ANALOG)

# Configure the selected pins in coordination with the alternate function table
Pin('C12',  mode=Pin.ALT, alt=7) # Set pin modes to UART matching column 7 in alt. fcn. table
Pin('D2', mode=Pin.ALT, alt=7)


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

ir_1 = 'A6'
ir_3 = 'A7'
ir_5 = 'C2'
ir_7 = 'B0'  # analog in
ir_9 = 'C4'
ir_11 = 'C3'
ir_13 = 'B1'  # analog in
ir_ctrl = 'B2'


enc_pins = [right_enc_A, right_enc_B, right_enc_timer, left_enc_A, left_enc_B, left_enc_timer]
motor_pins = [right_pwm_pin, right_dir_pin, right_slp_pin, right_pwm_timer, left_pwm_pin, left_dir_pin, left_slp_pin, left_pwm_timer]
qtr_pins = [ir_1, ir_3, ir_5, ir_7, ir_9, ir_11, ir_13]

right_motor = Motor([right_pwm_pin, right_dir_pin, right_slp_pin, right_pwm_timer],4)
left_motor = Motor([left_pwm_pin, left_dir_pin, left_slp_pin, left_pwm_timer],1)
right_motor.stop()
left_motor.stop()

i2c = I2C(3, I2C.CONTROLLER)  # Make sure you're using the correct I2C bus
sleep(1)  # Allow devices to power up

devices = i2c.scan()  # Scan for I2C devices
print(f"Detected I2C devices: {devices}")

if not devices:
    print("No I2C devices found")
else:
    print(f"Found I2C devices at addresses: {[hex(dev) for dev in devices]}")



encoder = EncoderTask(enc_pins)
motor = MotorTask(motor_pins[0:4], motor_pins[4:8], 4, 1)
data_collecting = DataCollectionTask()
qtr = QTRSensor(qtr_pins, ir_ctrl)
qtr_more = QTRTask(qtr)
control = ControlTask([20, 0, 0],0)  # [k_p, k_i, K_d], offset
#imu = BNO055(i2c, 'A15')
#imu_more = HeadingTask(imu)
#user_more = User(BT_ser)


if __name__ == '__main__':
    """
    Create shares, create tasks, append tasks
    """
    right_pos = task_share.Share('f', name='Right Encoder Pos')
    left_pos = task_share.Share('f', name='Left Encoder Pos')
    right_vel = task_share.Share('f', name='Right Encoder Vel')
    left_vel = task_share.Share('f', name='Left Encoder Vel')
    right_speed = task_share.Share('h', name="Right Speed")  # Input Speed for motor pwm [%]
    right_stop = task_share.Share('h', name="Right Stop")
    left_speed = task_share.Share('h', name="Left speed")  # Input Speed for motor pwm [%]
    left_stop = task_share.Share('h', name="Left Stop")
    right_speed.put(0)
    right_stop.put(1)
    left_speed.put(0)
    left_stop.put(1)
    right_mes_pos = task_share.Share('f', name="Right Mes Pos")
    left_mes_pos = task_share.Share('f', name="Left Mes Pos")
    right_mes_vel = task_share.Share('f', name="Right Mes Vel")
    left_mes_vel = task_share.Share('f', name="Left Mes Vel")
    times = task_share.Queue('h', 2000, name="Times")
    data_collect = task_share.Share('h', name="Data Collect?")
    rolling = task_share.Share('h', name="Rolling")
    error = task_share.Share('f', name="Error")
    heading_error = task_share.Share('f', name="Heading Error")
    user_input = task_share.Share('h', name="User Input")

    enc_task = cotask.Task(encoder.encoder_gen, name='Encoder Task', priority=1, period=1,
                           shares=([right_pos, right_vel, left_pos, left_vel]), trace=False, profile=True)

    motor_task = cotask.Task(motor.go, name='Motor Task', priority=1, period=8,
                           shares=([right_speed, left_speed, right_stop, left_stop]), trace=False, profile=True)
    controller_task = cotask.Task(control.controller, name='Control Task', priority=1, period=8, shares=[error, right_speed, left_speed], trace=False, profile=True)
    qtr_task = cotask.Task(qtr_more.get_line, name='QTR Task', priority=1, period=10, shares=error, trace=False, profile=True)
    #imu_task = cotask.Task(imu_more.get_heading, name='IMU Task', priority=1, period=8, shares=heading_error, trace=False, profile=True)
    #
    #user_task = cotask.Task(user_more.user, name='User Task', priority=3, period=1, shares=user_input, trace=False, profile=True)

    cotask.task_list.append(enc_task)
    cotask.task_list.append(qtr_task)
    cotask.task_list.append(controller_task)
    cotask.task_list.append(motor_task)
    #cotask.task_list.append(data_collect_task)
    #cotask.task_list.append(imu_task)
    right_speed.put(0)
    right_stop.put(1)
    left_speed.put(0)
    left_stop.put(1)

    # # Calibrate
    # print('place on white')
    # i = 0
    # sleep(3)
    # qtr.readIR()
    # white = qtr.values
    # print('place on black')
    # sleep(3)
    # qtr.readIR()
    # black = qtr.values
    # print(white)
    # print(black)
    # sleep(3)
    # white = [2476, 2051, 3875, 2108, 2028, 2134, 2109]
    # black = [3206, 2949, 3876, 3047, 2962, 3023, 2958]
    qtr.calibrate()
    interval = 1_000
    begin_time = ticks_ms()
    deadline = ticks_add(begin_time, interval)
    try:
        # right_speed.put(20)
        right_stop.put(0)
        # left_speed.put(20)
        left_stop.put(0)
        while True:
            now = ticks_ms()
            cotask.task_list.pri_sched()
            if ticks_diff(deadline, now) < 0:
                # print("Calibration Status:", imu.get_calibration_status())
                # print("Euler Angles:", imu.read_euler_angles())
                # print("Heading:", imu.read_heading())
                # print("Angular Velocity:", imu.read_angular_velocity())
                # print("Yaw Rate:", imu.read_yaw_rate())
                print(f'Error: {error.get()}')
                deadline = ticks_add(deadline, interval)
    except KeyboardInterrupt:
        print('done hopefully')
    right_speed.put(0)
    right_stop.put(1)
    left_speed.put(0)
    left_stop.put(1)
    print('\n' + str(cotask.task_list))
    print(task_share.show_all())
    print('')
    while True:
        cotask.task_list.pri_sched()
        pass
    


