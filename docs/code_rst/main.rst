main
====

Our main program initializes all class objects, tasks and shares. It then runs the scheduler
and jumps between states to complete the course.

Course Finite State Machine
...........................

.. code-block:: python

    print('Press button to start run')

    try:
        while True:
            cotask.task_list.pri_sched()
            """Print Section"""
            now = ticks_ms()
            if ticks_diff(deadline, now) < 0:
                print(
                    f'Right_Pos- thresh: {right_pos.get() - thresh}, State: {state}, R_speed: {right_speed.get()}, Heading: {heading.get()}')
                deadline = ticks_add(deadline, interval)

            """Course State machine

            Hardcoded states based on encoder position and bumper state.
            Jumps between line sensing and north sensing modes to complete the course.
            """

            if state == S0_wait_to_start:
                line_heading.put(4)
                if button_state != prev_button_state:
                    prev_button_state = button_state
                    sleep(.2)
                    state = S1_to_diamond
            elif button_state != prev_button_state:
                prev_button_state = button_state
                state = S0_wait_to_start

            if state == S1_to_diamond:
                line_heading.put(0)
                if rep == 0:
                    thresh = right_pos.get() + 5_500
                    heading_north = (imu.read_heading()+90)%360
                    print(f'Heading North: {heading_north}')
                    rep += 1

                if right_pos.get() > thresh:
                    state = S2_straightline_diamond
                    rep = 0

            if state == S2_straightline_diamond:

                if rep == 0:
                    line_heading.put(1)
                    hed_set = heading_north + 90

                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    heading_set.put(hed_set)
                    thresh = right_pos.get() + 1_000
                    print(f'Threshold: {thresh}, hed_set: {hed_set}')
                    rep += 1
                if right_pos.get() > thresh:
                    state = S3_to_grid
                    rep = 0
            if state == S3_to_grid:
                line_heading.put(0)
                if rep == 0:
                    thresh = right_pos.get() + 16_000
                    rep += 1
                if right_pos.get() > thresh:
                    state = S4_to_turn
                    rep = 0
            if state == S4_to_turn:
                line_heading.put(1)
                if rep == 0:
                    thresh = right_pos.get() + 4_000
                    hed_set = heading_north - 180
                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    heading_set.put(hed_set)
                    rep += 1
                if right_pos.get() > thresh:
                    state = S5_turn_1
                    right_speed.put(0)
                    left_speed.put(0)
                    rep = 0
            if state == S5_turn_1:
                if rep == 0:
                    hed_set = heading_north - 90
                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    heading_set.put(hed_set)
                    line_heading.put(2)
                    rep += 1
                if -10 < (hed_set - heading.get()) < 10:
                    right_speed.put(0)
                    left_speed.put(0)
                    state = S6_to_wall
                    rep = 0
            if state == S6_to_wall:
                line_heading.put(0)
                if bumper_state:
                    print(f'Bumper hit')
                    right_speed.put(0)
                    left_speed.put(0)
                    state = S7_reverse
            if state == S7_reverse:
                line_heading.put(3)

                if rep == 0:
                    thresh = right_pos.get() - 500
                    hed_set = heading_north - 90

                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    print(f'hed_set: {hed_set}')
                    heading_set.put(hed_set)
                    rep += 1
                if right_pos.get() < thresh:
                    right_speed.put(0)
                    left_speed.put(0)
                    state = S8_turn_2
                    rep = 0
            if state == S8_turn_2:
                line_heading.put(2)
                if rep == 0:
                    hed_set = heading_north
                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    heading_set.put(hed_set)
                    line_heading.put(2)
                    rep += 1
                if -10 < (hed_set - heading.get()) < 10:
                    right_speed.put(0)
                    left_speed.put(0)
                    state = S9_to_3
                    rep = 0
            if state == S9_to_3:
                line_heading.put(1)
                heading_set.put(heading_north)
                if rep == 0:
                    thresh = right_pos.get() + 2_000
                    rep += 1
                if right_pos.get() > thresh:
                    state = S10_turn_3
                    rep = 0
            if state == S10_turn_3:
                line_heading.put(2)
                if rep == 0:
                    hed_set = heading_north - 90
                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    heading_set.put(hed_set)
                    line_heading.put(2)
                    rep += 1
                if -10 < (hed_set - heading.get()) < 10:
                    right_speed.put(0)
                    left_speed.put(0)
                    state = S11_to_4
                    rep = 0
            if state == S11_to_4:
                line_heading.put(1)
                hed_set = heading_north - 90
                if hed_set < 0:
                    hed_set += 360
                elif hed_set > 360:
                    hed_set -= 360
                heading_set.put(hed_set)
                if rep == 0:
                    thresh = right_pos.get() + 2_000
                    rep += 1
                if right_pos.get() > thresh:
                    state = S12_turn_4
                    rep = 0
            if state == S12_turn_4:
                line_heading.put(2)
                if rep == 0:
                    hed_set = heading_north - 180
                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    heading_set.put(hed_set)
                    line_heading.put(2)
                    rep += 1
                if -10 < (hed_set - heading.get()) < 10:
                    right_speed.put(0)
                    left_speed.put(0)
                    state = S13_to_finish
                    rep = 0
            if state == S13_to_finish:
                if rep == 0:
                    hed_set = heading_north - 180
                    if hed_set < 0:
                        hed_set += 360
                    elif hed_set > 360:
                        hed_set -= 360
                    heading_set.put(hed_set)
                    line_heading.put(1)
                    thresh = right_pos.get() + 2_200
                    rep += 1
                if right_pos.get() > thresh:
                    state = S0_wait_to_start
                    rep = 0

                    print('Done!')



.. automodule:: main
   :members:
   :show-inheritance:
   :undoc-members:
