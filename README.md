# ME-405 Romi Term Project
### By: Andrew Carr and Alain Kanadjian
### Instructor: Charlie Refvem

---


This repository houses all documentation regarding our Romi project 
that was worked on throughout this quarter.

All documentation can be found here:

[ME-405 Romi Term Project Documentation](https://andrewpatcarr.github.io/ME405_Romi-Term-Project/)

### The Project

Throughout our quarter in ME-405, we worked on labs that used our mini-car robot, Romi, in different ways. 
We parameterized our motors, implemented task-based non-blocking programming, implemented an IR line sensor, and worked with an IMU. 
All of these labs were building towards our term project/challenge.

<img src="docs/_static/romi_pic_cropped.png" alt="romi_pic" width="800">

We were tasked with completing a complex track with obstacles, quick bends, and varying surface prints. 

<img src="docs/_static/game_track.png" alt="Game Track" width="800">

### Hardware

Our Pololu Romi has a STM-32 Nucleo with a Calpoly custom 'Shoe of Brian' along with a Pololu motor driver.

Romi has two DC motor driven wheels with quadrature encoders. We mounted an IMU for orientation sensing, 
an IR sensor to track a black line, and a bump sensor for impact sensing.

See cad and pinout folders for files and the [hardware](https://andrewpatcarr.github.io/ME405_Romi-Term-Project/hardware.html)
and [assembly](https://andrewpatcarr.github.io/ME405_Romi-Term-Project/assembly.html) pages for documentation.

### Programming

We structured our code using object-oriented programming principles and task-based architecture for
streamlined modifications and control. Each part of the robot runs as a separate task, allowing for easy 
debugging and organization. We use a PI controller to set motor speed based on encoder feedback. 
The encoder uses quadrature signals and an AR reset to prevent overflow. Our IR sensor uses a centroid-based 
algorithm to track black lines for navigation.

See the source code in the code folder and the [programming](https://andrewpatcarr.github.io/ME405_Romi-Term-Project/programming.html),
[control](https://andrewpatcarr.github.io/ME405_Romi-Term-Project/control_scheme.html), and
[code modules](https://andrewpatcarr.github.io/ME405_Romi-Term-Project/code_rst/modules.html) pages for detailed documentation.

