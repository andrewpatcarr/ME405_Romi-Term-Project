from pyb import Pin, Timer


slp_pin_1 = Pin("C2", mode=Pin.OUT_PP)
slp_pin_2 = Pin("B6", mode=Pin.OUT_PP)

slp_pin_1.high()
slp_pin_2.high()
