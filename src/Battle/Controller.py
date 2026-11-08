import pygame
pygame.joystick.init()

class Controller:
    """
    Reads a DualSense controller and maintains a list of currently pressed buttons.
    Compatible with Mega Man Battle Network-style input handling.
    """

    # Mapping of pygame joystick button indices → readable names
    BUTTON_MAP = {
        0: "cross",      # ✕
        1: "circle",     # ○
        2: "square",     # □
        3: "triangle",   # △
        4: "share",      # Create
        5: "ps",         # PlayStation button
        6: "options",    # Options
        7: "l3",         # Left stick click
        8: "r3",         # Right stick click
        9: "l1",         # L1
        10: "r1",        # R1
        11: "up",        # D-pad up
        12: "down",      # D-pad down
        13: "left",      # D-pad left
        14: "right",     # D-pad right
        15: "touchpad",  # Touchpad click
    }

    def __init__(self):
        self.dead_zone = 0.25  # lower valued inputs are ignored
        self.joystick = None

        if pygame.joystick.get_count() == 0:
            print("No controller detected.")
            return

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        print(f"Connected: {self.joystick.get_name()}")

    def get_pressed(self):
        """
        Call this every frame.
        Rebuilds the pressed_buttons list with every button currently held.
        """
        pressed_buttons = []
        if self.joystick is None:
            return pressed_buttons

        pygame.event.pump()  # Required so pygame updates joystick state

        # Digital buttons
        for i in range(self.joystick.get_numbuttons()):
            if self.joystick.get_button(i):
                name = self.BUTTON_MAP.get(i, f"button_{i}")
                pressed_buttons.append(name)

        # Analog triggers as digital (L2 / R2)
        # On DualSense, axes 4 and 5 are usually the triggers
        if self.joystick.get_numaxes() >= 6:
            l2 = self.joystick.get_axis(4)
            r2 = self.joystick.get_axis(5)

            if l2 > self.dead_zone:
                pressed_buttons.append("l2")
            if r2 > self.dead_zone:
                pressed_buttons.append("r2")

        # Optional: treat left stick as digital directions (useful for Battle Network style)
        if self.joystick.get_numaxes() >= 2:
            lx = self.joystick.get_axis(0)
            ly = self.joystick.get_axis(1)

            if lx < -self.dead_zone:
                pressed_buttons.append("left_stick_left")
            elif lx > self.dead_zone:
                pressed_buttons.append("left_stick_right")

            if ly < -self.dead_zone:
                pressed_buttons.append("left_stick_up")
            elif ly > self.dead_zone:
                pressed_buttons.append("left_stick_down")

        return pressed_buttons