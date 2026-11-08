from pygame import Surface
from src.utils import graphics as grp
from src.Battle.Warriors.Warrior import Warrior


class Player(Warrior):
    """
        This class implements the base of every playable character. Which includes the following:
        - Charging (L1) -> Progressively increase the amount of Mana but stops the energy recovery;
        - Blocking (R2) -> Blocks relatively low level enemy attacks but damage is still taken if enemies are stronger;
        - Movement (Arrows) -> Move in the direction of the pressed arrow. This action uses Energy and has a cooldown;
    """

    def __init__(self):
        super().__init__(2, 2)
        self.coo = self.get_pixel_coordinates()  # coordinates on the screen (where to display the image)
        self.images = {"idle": grp.load_image("Battle/Characters/BlackKnight/Idle.png"),
                       "charging": grp.load_image("Battle/Characters/BlackKnight/Charging.png"),
                       "block": grp.load_image("Battle/Characters/BlackKnight/Block.png"),
                       "attack": grp.load_image("Battle/Characters/BlackKnight/Magic.png")
                       }
        self.state = "idle"  # must be a string that is present as a key in the self.images dictionary

        self.MAX_HP =  100
        self.hp = self.MAX_HP
        self.MAX_ENERGY = 100
        self.energy = self.MAX_ENERGY
        self.MAX_MANA = 100
        self.mana = 0
        self.MAX_SKILL_POINTS = 10
        self.skill_points = self.MAX_SKILL_POINTS
        self.movement_energy_cost = 10  # Amount of energy consumed by moving to another tile
        self.energy_charging_speed = 15  # Speed in energy/second regained by charging
        self.energy_depletion_cooldown_time = 0  # Energy restores after this clock arrives to 0
        self.ENERGY_DEPLETION_TOTAL_COOLDOWN_TIME = 2  # Total time (seconds) to wait after energy depletion before recharging
        self.mana_charging_speed = 40  # Speed of mana gained by charging (Mana/Second)
        self.mana_discharging_speed = 20   # Speed at which mana is lost when not charging (Mana/Second)
        # DEPRECATED: The property energy_charging_speed is added to the desired speed so that it cancels out
        self.block_energy_consumption_speed = 20  # Speed at which energy is lost when blocking (Jolt/Second)
        self.mana_conservation_interval = 0  # Clock that keeps how much time the player has left before mana decreases
        self.movement_current_cooldown_time = 0  # Time left to wait (Seconds) before moving again
        self.MOVEMENT_TOTAL_COOLDOWN_TIME = 1  # Amount in seconds that the player must wait before moving again

        self.attack_energy_charging_cooldown_time = 0
        self.ATTACK_ENERGY_CHARGING_MAX_TIME = 1.5  # Amount in seconds before the energy starts recharging after an attack

        self.charging_animation = ChargingAnimation("Battle/Characters/Charging", (350, 380), 47, (self.coo[0]-130, self.coo[1]-140))
        self.player_actions = {"l1": self.charge, "r1": self.attack, "r2": self.block}
        self.dt = 0  # This is the last provided delta-time. It is used internally to make the elements frame-independent

    def get_pixel_coordinates(self):
        """
            The x and y properties of the player are the coordinates of the cell on which the player is located.
            This function converts those coordinates to pixel coordinates in order to pygame to display the player's image
        """
        return self.x*128, self.y*-100+505

    def add_hp(self, value: float):
        raise Exception("NotImplemented")  # Implemented at the class AttackPlayer

    def add_energy(self, value: float):
        raise Exception("NotImplemented")  # Implemented at the class AttackPlayer

    def add_mana(self, value: float):
        raise Exception("NotImplemented") # Implemented at the class AttackPlayer

    def manage_movement(self, pressed_buttons: list) -> bool:
        """
            Moves the Player along the Battle Grid according to the pressed buttons.
            The Player is kept in the Boundaries of the Grid AND of its range (Which in-game actions can change)
            In case of movement True is returned and False if not
        """
        has_moved = False
        if self.y > 0 and "down" in pressed_buttons:
            self.y -= 1
            has_moved = True
        elif self.y < 3 and "up" in pressed_buttons:
            self.y += 1
            has_moved = True
        elif self.x > 0 and "left" in pressed_buttons:
            self.x -= 1
            has_moved = True
        elif self.x <= self.PLAYER_FIELD_RANGE and "right" in pressed_buttons:
            self.x += 1
            has_moved = True

        if has_moved:
            self.movement_current_cooldown_time = self.MOVEMENT_TOTAL_COOLDOWN_TIME
            self.add_energy(-self.movement_energy_cost)
            self.coo = self.get_pixel_coordinates()
            self.charging_animation.coo = (self.coo[0]-130, self.coo[1]-140)

        return has_moved

    def charge(self):
        """
            When the player charges, the amount of Mana he has rises at a steady continuous manner until reaching a limit.
            When the mana reaches its maximum, the player enters Max-Mana state for a short period of time.
            Some Special Attacks only work when in this state.
            In the future, the weapons that reached the limit of their upgrade, should unlock a Mana-Using Special Attack
        """
        self.state = "charging"
        # there is no need to increment if at max energy
        # stops cheating by spamming charge
        if self.mana < self.MAX_MANA and self.charging_animation.current_frame > 2:  # and self.state == "charging" must be charging in order to charge
            self.add_mana(self.mana_charging_speed*self.dt)

            if self.mana == self.MAX_MANA:
                self.mana_conservation_interval = 1.5

    def attack(self):
        """
            The player is able to perform attacks to damage the Enemies.
            An attack uses a discrete amount of Energy According to the type of weapon used.
            The player can utilize different weapons, which can perform up to 4 types of attacks.
            This is only the Base Player Class, Therefore this method only implements what is common among Player Classes.
        """
        # The energy of the player only rises if the attack button is released.
        # This means that the player has to be informed the attack button is not working at that moment
        # Therefore, the player is forced to an Idle state when:
        # The energy reaches 0 AND half the time for the energy to restart rising has passed
        if self.energy <= 0 and self.energy_depletion_cooldown_time <= self.ENERGY_DEPLETION_TOTAL_COOLDOWN_TIME*0.5:
            self.state = "idle"
            # The following line avoids a transition glitch between the idle and block animations
            # This happens when trying to block with 0 energy.
            # The solution is to compensate for the time gained in the self.update method
            self.energy_depletion_cooldown_time += self.dt
            # audio clue to inform the action is not allowed.
            # In order not to spam a noise, use an audio with a certain amount of silence at the end and loop it
            return
        self.state = "attack"

    def block(self):
        """
            The player is able to block incoming attacks. This uses Energy at a certain rate.
        """
        if self.energy > 0:
            self.state = "block"
            self.add_energy(-self.block_energy_consumption_speed * self.dt)
            return

        self.state = "idle"
        # The following line avoids a transition glitch between the idle and block animations
        # This happens when trying to block with 0 energy.
        # The solution is to compensate for the time gained in the self.update method
        self.energy_depletion_cooldown_time += self.dt
        # audio clue to inform the action is not allowed
        # In order not to spam a noise, use an audio with a certain amount of silence at the end and loop it

    def act(self, pressed_buttons: list) -> None:
        """
            All the actions performed by the player are implemented in this class.
            When a Button is pressed, the player will act accordingly to what is implemented in this method.
        """
        if self.state == "idle" or self.state == "attack":
            # the Player is only able to move after a certain amount of time after the last movement
            # and only if he has the required energy to do so
            if self.movement_current_cooldown_time <= 0 < self.energy:
                player_has_moved = self.manage_movement(pressed_buttons)
                # if the Player has moved, there is no need to check for other inputs
                if player_has_moved:
                    return

        # Using a for-loop guarantees that the actions will take place in a FIFO manner regarding the pressed buttons
        for pressed_button in pressed_buttons:
            # Only do something for the implemented actions (the ones in the self.player_actions dictionary)
            if pressed_button in self.player_actions:
                self.player_actions[pressed_button]()
                return  # these actions nullify all later inputs

        # Only Special Attacks can make the player not revert back to the Idle state when no button is pressed
        if self.state != "special_attack":
            self.state = "idle"
            self.charging_animation.reset()

    def update(self, dt: float):
        """
            This function updates the player on a Frame-By-Frame basis. Only the ESSENTIAL STUFF should be here!
        """
        self.dt = dt  # now this is the last known dt
        self.movement_current_cooldown_time -= dt
        self.energy_depletion_cooldown_time -= dt
        self.attack_energy_charging_cooldown_time -= dt

        if self.state != "charging":
            # The player has a certain amount of time before the mana starts decreasing
            self.mana_conservation_interval -= self.dt
            if self.mana_conservation_interval <= 0:
                self.add_mana(-self.mana_discharging_speed*self.dt)
            # The player progressively regains Energy

        if self.state != "block":
            if self.state == "attack" and self.attack_energy_charging_cooldown_time > 0:
                return
            self.add_energy(self.energy_charging_speed * self.dt)

    def draw(self, screen: Surface):
        """
            Display the player and all his related visual attributes on the screen.
        """
        screen.blit(self.images[self.state], self.coo)
        if self.state == "charging":
            self.charging_animation.draw(screen)


class ChargingAnimation:
    def __init__(self, folder: str, size: tuple, frame_number: int, coo: (int, int)):
        self.size = size
        self.frames = [grp.load_image(f"{folder}/{i}.png", size) for i in range(frame_number-1)]
        self.current_frame = 0
        self.first_loop = True
        self.coo = coo

    def draw(self, screen: Surface):
        # Avoid displaying the empty frames (0 and 1) during the charging animation
        if not self.first_loop and self.current_frame < 2 :
            self.current_frame = 2
        # After the first two frames, the animation can be considered on the next cycle even if it is technically not
        if self.current_frame > 2:
            self.first_loop = False

        screen.blit(self.frames[int(self.current_frame)], self.coo)
        self.current_frame = (self.current_frame+0.2)%len(self.frames)

    def reset(self):
        self.current_frame = 0
        self.first_loop = True