Control
=======

Our Romi is a relatively linear system with mostly simple sensors which points us to the
ever-reliable PID controller. Due to the noise of most of our signals, we decided to use PI control. However, during
testing, a well tuned proportional controller was good enough. If we had more time and were tasked to optimize our time
on the course, we would implement integral control to reduce the jumpyness and steady state error we sometimes
experienced.

We have a cascading control scheme that closes the loop with multiple sensors.
Our controller starts with a path pointing sensor such as our line sensor or the heading
reading from our IMU. This signal is processed to tell each motor what speed it should
go to achieve the goal of our outmost controller.

The speeds that are sent to the
motors are monitored by another controller via the encoder. This allows us to accurately
follow a line, go in a straight line and individually tune each system.


.. image:: _static/romi_block_diagram_course.png
   :width: 800px
   :alt: ControlBlockDiagram
