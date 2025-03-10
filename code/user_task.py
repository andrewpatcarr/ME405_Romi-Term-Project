from pyb import USB_VCP


class User:
    def __init__(self, ser):
        self.ser = ser

        self.S0_init = 0
        self.S1_init = 1
        self.state = self.S0_init
        self.char_in = '0'

    def user(self, shares):
        user_input = shares
        while True:
            if self.state == self.S0_init:
                yield self.state
            elif self.state == self.S1_init:
                if self.ser.any():  # wait for any character
                    self.char_in = self.ser.read(1).decode()
                    if self.char_in == "\n":
                        print('return inputted')
                        user_input.put(1)
                yield self.state
