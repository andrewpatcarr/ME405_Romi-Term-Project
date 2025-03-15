Hardware
========


Components
----------

.. list-table::
   :widths: 50 20 50
   :header-rows: 1

   * - Item
     - Quantity
     - Notes
   * - `Romi Chassis Kit <https://www.pololu.com/category/203/romi-chassis-kits>`_
     - 1
     - A differential-drive mobile robot platform.
   * - `Romi Ball Caster Kit <https://www.pololu.com/category/204/romi-chassis-components>`_
     - 1
     - Provides a third point of contact for the robot.
   * - `Snap-Action Switch with 18.5mm Bump Lever <https://www.pololu.com/product/1405>`_
     - 1
     - A single-pole, double-throw momentary switch used as a tactile bump sensor for physical collisions.
   * - `QTR-MD-13A Reflectance Sensor Array <https://www.pololu.com/product/4253>`_
     - 1
     - A 13-channel array of IR LED/phototransistor pairs with 4mm length, used for precise line detection and following.
   * - `Gearmotor and Encoder Assembly for Romi/TI-RSLK MAX <https://www.pololu.com/product/3675>`_
     - 2


Romi
----
Romi is a small differential drive robot that uses two wheels powered by DC motors with encoders. Romi has a Shoe of Brian and Nucleo-L476RG along with attached components like a bump sensor, QTR sensor, and IMU. The plastic chassis is lightweight allowing easier configuration and navigation. The two DC motors are connected to a gearbox for proper torque, controlled by pulse width modulation signals, allowing for variable speed control. The encoders connected to the motors allow for a closed feedback loop, so we can implement motion tracking and autonomous movement. The motor driver controls the voltage and current to each motor, allowing for bidirectional movement and speed control. 
<add stuff about base romi, wheel motors, motor driver>

`Video of test <https://youtube.com/shorts/lIelwNlQIkY>`_

STM-32 Nucleo
-------------
The STM32 Nucleo is the main microcontroller for Romi. The board has an ARM processor, various GPIO pins, and interfaces for I2C, SPI, and UART. The Nucleo allows for real time data processing, sensor integraiton and motor control through MicroPython.

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
The bump sensor uses a gate switch to detect physical collisions in the robot's path. We integrated the sensor using a 3D printed part. When the bump sensor is activated, it sends a signal to the microcontroller, which when then have the robot reverse and reapproach the obstacle. This is essential for navigating the course for what the IR sensor cannot detect.
<add stuff about bump sensor, cad, how it work>



