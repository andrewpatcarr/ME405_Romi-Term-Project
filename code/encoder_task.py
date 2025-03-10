from encoder import Encoder

class EncoderTask:
    """
    A class to handle reading the encoder.

    Attributes
        right_enc_A (int): The pin for channel A for the right wheel encoder.
        right_enc_B (int): The pin for channel B for the right wheel encoder.
        right_enc_timer (int): The channel timer number for the right wheel encoder.
        left_enc_A (int): The pin for channel A for the left wheel encoder.
        left_enc_B (int): The pin for channel B for the left wheel encoder.
        left_enc_timer (int): The pin channel timer number for the left wheel encoder.
        S0_init (int): Initialization state value.
        S1_init (int): Read state value.
        state (int): Current state value.

        right_encoder (Encoder): Encoder class object for the right wheel encoder.
        left_encoder (Encoder): Encoder class object for the left wheel encoder.

    Methods
        encoder_gen (shares: list) --> state:
            Jumps between states to initialize and read encoder values.
    """
    def __init__(self, pins):
        """
        Initializes the EncoderTask object and creates Encoder classes for each encoder.

        Args:
            pins (list): The values for encoder channels and timers.
        """

        right_enc_A = pins[0]
        right_enc_B = pins[1]
        right_enc_timer = pins[2]
        left_enc_A = pins[3]
        left_enc_B = pins[4]
        left_enc_timer = pins[5]
        self.S0_init = 0
        self.S1_read = 1

        self.state = self.S0_init

        self.right_encoder = Encoder(right_enc_A, right_enc_B, right_enc_timer)
        self.left_encoder = Encoder(left_enc_A, left_enc_B, left_enc_timer)
    def encoder_gen(self, shares):
        """
        The function that implements the finite state machine for the Encoder task.

        Args:
            shares (list): shared values for position and velocity for each wheel.
        """
        right_pos, right_vel, left_pos, left_vel = shares
        while True:
            # print('in encoder task')
            if self.state == self.S0_init:
                self.right_encoder.zero()  # Reset right encoder
                self.left_encoder.zero()   # Reset left encoder
                self.state = self.S1_read
                yield self.S1_read

            if self.state == self.S1_read:
                self.right_encoder.update()
                self.left_encoder.update()
                # Read right encoder
                right_pos.put(self.right_encoder.get_position())
                right_vel.put(self.right_encoder.get_velocity())
                # Read left encoder
                left_pos.put(self.left_encoder.get_position())
                left_vel.put(self.left_encoder.get_velocity())
                # print(f'Right Pos: {right_pos.get()}')
                yield self.S1_read
                