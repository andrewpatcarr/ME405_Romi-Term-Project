import time
import struct
from pyb import Pin, I2C
i2c = I2C(3, I2C.CONTROLLER)  # Make sure you're using the correct I2C bus
time.sleep(1)  # Allow devices to power up

devices = i2c.scan()  # Scan for I2C devices
print(f"Detected I2C devices: {devices}")

if not devices:
    print("No I2C devices found")
else:
    print(f"Found I2C devices at addresses: {[hex(dev) for dev in devices]}")



class BNO055:
    """A driver class for the BNO055 IMU using I2C communication."""

    I2C_ADDR = 0x28  # Default I2C address for the BNO055
    #I2C_ADDR=0x29
    OPR_MODE_REG = 0x3D
    CALIB_STAT_REG = 0x35
    EULER_H_LSB_REG = 0x1A
    GYRO_DATA_LSB_REG = 0x14
    CALIB_DATA_REG = 0x55

    CONFIG_MODE = 0x00
    NDOF_MODE = 0x0C  # Sensor fusion mode

    def __init__(self, i2c, reset_pin):
        """
        Initializes the BNO055 sensor.

        :param i2c: An initialized I2C object.
        :param reset_pin: The reset pin (active low).
        """
        self.i2c = i2c
        self.reset_pin = Pin(reset_pin, Pin.OUT_PP)
        self.reset_pin.high()
        self.i2c.mem_write(0x0C,self.I2C_ADDR,0x3D)
        time.sleep(0.75)
        #self.reset()

    def reset(self):
        """Resets the BNO055 using the reset pin."""
        self.reset_pin.low()
        time.sleep(0.01)
        self.reset_pin.high()
        time.sleep(0.75)  # Allow time for reboot

    def set_mode(self, mode):
        """Set the operation mode with retry on failure."""
        self.mode=mode
        self.i2c.mem_write(self.mode,self.I2C_ADDR,0x3D)
        time.sleep(0.05)
        

    def get_calibration_status(self):
        """
        Reads and returns the IMU calibration status.

        :return: A tuple (system, gyroscope, accelerometer, magnetometer) with values 0-3.
        """
        status=self.i2c.mem_read(1,self.I2C_ADDR,0x35)[0]
        bit,=struct.unpack('<B',status)
        system=(bit>>6) & 0x03
        gyro=(bit>>4) & 0x03
        acct=(bit>>2) & 0x03
        magnet=bit & 0x03
        return system,gyro,acct,magnet
        #status = self.i2c.mem_read(1, self.I2C_ADDR, self.CALIB_STAT_REG)[0]
        #return (status >> 6) & 0x03, (status >> 4) & 0x03, (status >> 2) & 0x03, status & 0x03

    def read_euler_angles(self):
        """
        Reads and returns Euler angles (heading, roll, pitch) in degrees.

        :return: A tuple (heading, roll, pitch) in degrees.
        """
        data = self.i2c.mem_read(6, self.I2C_ADDR, 0x1A)
        heading, roll, pitch = struct.unpack('<hhh', data)
        return heading / 16.0, roll / 16.0, pitch / 16.0

    def read_heading(self):
        """
        Reads and returns only the heading angle in degrees.

        :return: Heading in degrees.
        """
        data = self.i2c.mem_read(2, self.I2C_ADDR, 0x1A)
        heading, = struct.unpack('<h', data)
        return heading / 16.0

    def read_angular_velocity(self):
        """
        Reads angular velocity data (gyro X, Y, Z).

        :return: A tuple (gyro_x, gyro_y, gyro_z) in degrees per second.
        """
        data = self.i2c.mem_read(6, self.I2C_ADDR, 0x14)
        gyro_x, gyro_y, gyro_z = struct.unpack('<hhh', data)
        return gyro_x / 16.0, gyro_y / 16.0, gyro_z / 16.0

    def read_yaw_rate(self):
        """
        Reads and returns only the yaw rate from the gyroscope.

        :return: Yaw rate in degrees per second.
        """
        data = self.i2c.mem_read(2, self.I2C_ADDR, 0x18)  # Z-axis gyro
        yaw_rate, = struct.unpack('<h', data)
        return yaw_rate / 16.0

# Example Usage
if __name__ == "__main__":
    i2c = I2C(1, I2C.CONTROLLER) #baudrate=
    imu = BNO055(i2c, "C9")  # Reset pin example
    
    imu.set_mode(BNO055.NDOF_MODE)
    print("Calibration Status:", imu.get_calibration_status())
    print("Euler Angles:", imu.read_euler_angles())
    print("Heading:", imu.read_heading())
    print("Angular Velocity:", imu.read_angular_velocity())
    print("Yaw Rate:", imu.read_yaw_rate())
