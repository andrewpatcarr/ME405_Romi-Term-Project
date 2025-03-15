.. ME-405 Term Project documentation master file, created by
   sphinx-quickstart on Sat Mar  8 17:24:39 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ME-405 Term Project Documentation
=================================
**By: Andrew Carr and Alain Kanadjian**

**Instructor: Charlie Refvem**


The Project - Romi
------------------

Throughout the quarter in ME-405, we worked on labs that built, wired, and programmed our mini-car robot, Romi, in different ways
for different tasks.

.. image:: _static/romi_pic_cropped.png
   :width: 800px
   :alt: GameTrack

We parameterized our motors, implemented task-based non-blocking programming, implemented an IR line sensor,
and worked with an IMU. All of these labs were building towards our term project/challenge. We needed to complete
the following course by hitting each checkpoint, detecting the wall and making our way back to the start pad.

Course
------

.. image:: _static/game_track.png
   :width: 800px
   :alt: GameTrack

Successful Run
--------------

After many many trials, debugging, reworking control methods, hardcoding distances, we were able to complete the course.

.. youtube:: lIelwNlQIkY
   :width: 510
   :height: 907

(Yes, we barely made it back on the pad but we are counting it :))

In this documentation, we will talk about the hardware and software of Romi. There is documentation regarding how our programs,
the drivers we created for each component, and the controllers we implemented.

Contents
--------

.. toctree::
   :maxdepth: 2

   hardware.rst
   assembly.rst
   control_scheme.rst
   programming.rst
   code_rst/modules

