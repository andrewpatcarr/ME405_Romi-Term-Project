from pyb import Pin, Timer, ADC
from time import ticks_us, ticks_diff, ticks_add, sleep, time, ticks_ms

class QTRSensor:
    """
    A class to handle QTR Reflectance Array Sensors.

    Attributes
    ----------
    pins : list
        pin values for each IR LED and the control pin.
    control : Pin
        Pin object for the control pin.
    white : list
        calibration readings for white background.
    black : list
        calibration readings for black background.

    Methods
    -------
    readIR()
        Read QTR sensors, normalize, and compute centroid.
    readRaw
        Read raw sensor values from QTR sensors.
    centroid()
        Return the current computed centroid value.
    calibrate_white()
        Read raw sensor values and set white calibration values.
    calibrate_black()
        Read raw sensor values and set black calibration values.


    """
    def __init__(self, pins,ctrl):
        self.pins = [ADC(pin) for pin in pins]  # Create ADC objects for each pin
        self.control=Pin(ctrl,mode=Pin.OUT_PP)
        self.control.high()
        self.white = [695, 320, 478, 364, 506, 386, 542]
        self.black = [2674, 2327, 2235, 2427, 2700, 2648, 2635]

    
    def readIR(self):
        """
        Reads all 7 Ir sensors and computes the centroid
        """
        self.control.high()
        sleep(0.0001)
        self.values = [pin.read() for pin in self.pins]
        #print(f'Values in qtr: {self.values}')
        self.values = [a - b for a,b in zip(self.values,self.white)]
        self.black = [a - b for a, b in zip(self.black, self.white)]
        self.values = [a/b for a,b in zip(self.values,self.black)]
        #self.normvalues=[value/4095 for value in self.values]
        
        #print(f'Values in qtr: {self.values}')
        self.weight = [-9,-6, -3, 0, 3, 6, 9]  # Sensor positions (adjust based on layout)

        self.numerator = sum(w * v for w, v in zip(self.weight, self.values))
        self.denominator = sum(self.values)
        self.P = self.numerator / self.denominator if self.denominator != 0 else 0
        
        self.control.low()

    def readRaw(self):
        self.control.high()
        sleep(0.0001)
        vals = [pin.read() for pin in self.pins]
        self.control.low()
        return vals

    def centroid(self):
        return self.P

    def calibrate_white(self):
        """
        Calibrates IR sensor
        Sets white and black set-points for readings
        """
        self.white = self.readRaw()

    def calibrate_black(self):
        """
        Calibrates IR sensor
        Sets white and black set-points for readings
        """

        self.black = self.readRaw()
        print(f'white: {self.white}')
        print(f'black: {self.black}')


class QTRTask:
    """
    A class to handle QTR Reflectance Array Sensors.

    Attributes
    ----------
    qtr_array : list
        Normalized sensor readings for each sensor.
    S0_init : int
        State 0 value for initialization.
    S1_read : int
        State 1 value for reading.
    state : int
        State of the FSM.
    """

    def __init__(self, qtr_array):
        self.qtr_array = qtr_array
        self.S0_init = 0
        self.S1_read = 1
        self.state = self.S0_init

    def get_line(self, shares):
        """
        The generator that implements teh FSM for the QTR task.

        State 0 initializes the generator. State 1 reads the sensor and computes the
        centroid which corresponds to the current error.

        Parameters
        ----------
        shares : int
            Line error shared variable for controller.

        Yields
        ------
        state : int
            The value of the current state within the machine
        """
        line_error = shares
        while True:
            if self.state == self.S0_init:
                self.state = self.S1_read
                yield self.state
            elif self.state == self.S1_read:
                self.qtr_array.readIR()  # Causes issue
                centroid = self.qtr_array.centroid()
                #print(f'Centroid: {centroid}')
                # center should be 7, positive value means needs to turn right, vice versa
                cent_error = centroid #- 7
                line_error.put(cent_error)
                #print(f'Cent Error: {cent_error}')
                #print(f'Readings: {self.qtr_array.values}')
                yield self.state
