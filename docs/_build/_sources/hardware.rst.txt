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
   * - `QTR-HD-13A Reflectance Sensor Array <https://www.pololu.com/product/4213>`_
     - 1
     - A 13-channel array of IR LED/phototransistor pairs with 4mm length, used for precise line detection and following.
   * - `Gearmotor and Encoder Assembly for Romi/TI-RSLK MAX <https://www.pololu.com/product/3675>`_
     - 2
     -  Gearmotors with encoders pre-installed, providing feedback for precise motor control
   * - `Adafruit BNO055 IMU <https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/overview>`_
     - 1
     - 9-DOF absolute orientation sensor
   * - `STM32 NUCLEO-L476RG <https://www.st.com/en/evaluation-tools/nucleo-l476rg.html>`__
     - 1
     - Microcontroller Dev Board


Romi
----
Romi is a small differential drive robot that uses two wheels powered by DC
motors with encoders. Romi has a Shoe of Brian and Nucleo-L476RG along with
attached components like a bump sensor, QTR sensor, and IMU. The plastic
chassis is lightweight allowing easier configuration and navigation. The
two DC motors are connected to a gearbox for proper torque, controlled by
pulse width modulation signals, allowing for variable speed control. The
encoders connected to the motors allow for a closed feedback loop, so we
can implement motion tracking and autonomous movement. The motor driver
controls the voltage and current to each motor, allowing for bidirectional
movement and speed control.


STM-32 Nucleo
-------------
Our Romi uses a STM32 Nucleo (particularly the `NUCLEO-L476RG <https://www.st.com/en/evaluation-tools/nucleo-l476rg.html>`_)
as its microcontroller. The board has an ARM processor, various GPIO pins,
and interfaces for I2C, SPI, and UART. The Nucleo allows for real time data processing, sensor
integration and motor control through MicroPython.

QTR Sensor
----------
The QTR sensor has an array of infrared reflectance sensor for line following, consisting of an IR LED
and phototransistor to detect reflectance of the surface it is pointed at. White surfaces return high readings,
while black surfaces return low readings. This sensor helps ROMI implement PID line following, adjusting motor
speeds based on intensity of reflected light to the sensor.

.. image:: _static/qtr_pic.jpg
   :width: 600px
   :alt: QTR Sensor

Image used from `pololu.com <https://a.pololu-files.com/picture/0J9915.1200.jpg?cc7523ea26737e153f8346b5d38e696a>`_.

IMU
---
We use an inertial measurement unit to track acceleration, angular velocity, and magnetic field heading.
Romi uses a BNO055 from adafruit which is a 9-DOF absolute orientation sensor using an accelerometer,
gyroscope and a magnetometer. This allows us to track orientation, follow angles relative to north,
and any environmental disturbances. We use I2C to communicate between our microcontroller and the IMU.

.. image:: _static/imu_pic.jpg
   :width: 600px
   :alt: IMU

Image used from `adafruit.com <https://learn.adafruit.com/assets/24585>`_.

Bump Sensor
-----------
The bump sensor uses a gate switch to detect physical collisions in the robot's path. We integrated the sensor
using a 3D printed part. When the bump sensor is activated, it sends a signal to the microcontroller, which when
then have the robot react to its situation. In the course, this meant the robot would reverse before going around
the wall. This adds another sense to our robot which is essential to navigate the final course.

Bump Sensor CAD
---------------

.. image:: _static/bump_sensor_cad.png
   :width: 800px
   :alt: Bump Sensor CAD



