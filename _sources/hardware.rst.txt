Hardware
========


Components
----------

.. list-table::
   :widths: 50 20 50
   :header-rows: 1

   * - Item
     - #
     - Notes
   * - `Romi Chassis Kit <https://www.pololu.com/category/203/romi-chassis-kits>`_
     - 1
     - blah blah
   * - `Romi Ball Caster Kit <https://www.pololu.com/category/204/romi-chassis-components>`_
     - 1
     - blah blah


Romi
----
Romi is a small differential drive robot that uses two wheels powered by DC motors with encoders. Romi has a Shoe of Brian and Nucleo-L476RG along with attached components like a bump sensor, QTR sensor, and IMU. The plastic chassis is lightweight allowing easier configuration and navigation. The two DC motors are connected to a gearbox for proper torque, controlled by pulse width modulation signals, allowing for variable speed control. The encoders connected to the motors allow for a closed feedback loop, so we can implement motion tracking and autonomous movement. The motor driver controls the voltage and current to each motor, allowing for bidirectional movement and speed control. 
<add stuff about base romi, wheel motors, motor driver>

`Link test <http://google.com>`_

STM-32 Nucleo
-------------
The STM32 Nucleo is the main microcontroller for Romi. The board has an ARM processor, various GPIO pins, and interfaces for I2C, SPI, and UART. The Nucleo allows for real time data processing, sensor integraiton and motor control through MicroPython.
<add stuff about this>

QTR Sensor
----------
The QTR sensor has an array of infared reflectance sensor for line following, consisting of an IR LED and phototransistor to detect reflectance of the surface it is pointed at. White surfaces return high readings, while black surfaces return low readings. This sensor helps ROMI implement PID line following, adjusting motor speeds based on intensity of relfected light to the sensor.
<add stuff about how it works, i think not talk about code in this but in other section but idk>

IMU
---
We use an intertial measurement unit to track acceleration, angular velocity, and magnetic field heading. Romi uses a BNO055 which allows us to track orientation, feedback, and any environmental disturbances. We use I2C to communicate for motion planning and course corrections.
<add stuff about the imu, how it works etc.>

Bump Sensor
-----------
The bump sensor uses a gat switch to detect physical collisions in the robot's path. We integrated the sensor using a 3D printed part. When the bump sensor is activated, it sends a signal to the microcontroller, which when then have the robot reverse and reapproach the obstacle. This is essential for navigating the course for what the IR sensor cannot detect.
<add stuff about bump sensor, cad, how it work>



