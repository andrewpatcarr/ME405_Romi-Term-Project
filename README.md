# ME-405 Romi Term Project
### By: Andrew Carr and Alain Kanadjian
### Instructor: Charlie Refvem

---


This repository houses all documentation regarding our Romi project 
that was worked on throughout this quarter.

All documentation, theory and resources can be found here:

[ME-405 Romi Term Project Documentation](https://andrewpatcarr.github.io/ME405_Romi-Term-Project/)

### The Project

Throughout our quarter in ME-405, we worked on labs that used our mini-car robot, Romi, in different ways. 
We parameterized our motors, implemented task-based non-blocking programming, implemented an IR line sensor, and worked with an IMU. 
All of these labs were building towards our term project/challenge.

//insert good photo of romi

We were tasked with completing a complex track with obstacles, quick bends and varying surface prints. 

<img src="readme-assets/game_track.png" alt="Game Track" width="800">

### Hardware

Our Pololu Romi has a STM-32 Nucleo with a Calpoly custom 'Shoe of Brian' along with a Polou motor driver.

Romi has two DC motor driven wheels with quadrature encoders. We mounted an IMU for orientation sensing, an IR sensor to track a black line, and a bump sensor for impact sensing.

// talk briefly about each electronic

### Programming

// talk about code style (OOP, tasks, etc.)
We structured our code using Object-Oriented Programming principles and use task based architecture for streamlined modifications and control. Each part of the robot runs as a seperate task, allowing for easy debugging and organization. Motor Control uses a PI controller to set motor speed based on encoder feedback. The encoder uses quadrature signals and an AR reset to prevent overflow. Our IR sensor uses a centroid based algorithm to track black lines for navigation.
// talk briefly about some of the main files like PI control, IR sensor centroid stuff,
encoder stuff(maybe the AR fixing), motor controlling

// Everything should be relatively brief -- point to the documentation on sphinx for more detail,
maybe we don't even talk about the specifics of the code here and do it all on the documentation
