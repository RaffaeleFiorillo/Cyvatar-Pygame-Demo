import pygame
from .AttackPlayer import AttackPlayer
import src.utils.graphics as grp
from src.app_config import SCREEN_WIDTH
from src.utils.common import randint


class BlasterPlayer(AttackPlayer):
    def __init__(self):
        pose_image_dir = f"Battle/Characters/BlackKnight/Shooting.png"
        am_names = [BoltBullet.NAME, ElectronBullet.NAME, QuantumBullet.NAME]
        super().__init__(pose_image_dir, "Blaster", 1, am_names)
        self.unique_properties_initialization()

    def unique_properties_initialization(self):
        self.update_weapon_coo()
        self.attack_modes = {0: self.attack_mode_1, 1: self.attack_mode_2, 2: self.attack_mode_3, 3: self.attack_mode_4}

    def update_weapon_coo(self):
        self.weapon_coo = (self.coo[0]+90, self.coo[1]+35)

    def attack_mode_1(self):
        """
            This attack shots a Big Bolt of Electricity which is not very fast, but deals a great deal of damage.
            After each bolt has been shot, there is a cooldown time before the next bolt can be shot
        """
        self.shooting_current_cooldown_time = BoltBullet.COOLDOWN_TIME
        self.damagers.append(BoltBullet((self.coo[0] + 120 + 15 * self.weapon_level, self.coo[1] + 45)))
        self.add_energy(-BoltBullet.ENERGY_COST)

    def attack_mode_2(self):
        self.shooting_current_cooldown_time = ElectronBullet.COOLDOWN_TIME
        self.damagers.append(ElectronBullet((self.coo[0] + 120 + 15 * self.weapon_level, self.coo[1] + 45)))
        self.add_energy(-ElectronBullet.ENERGY_COST)

    def attack_mode_3(self):
        self.shooting_current_cooldown_time = QuantumBullet.COOLDOWN_TIME
        self.damagers.append(QuantumBullet((self.coo[0] + 120 + 15 * self.weapon_level, self.coo[1] + 45)))
        self.add_energy(-QuantumBullet.ENERGY_COST)

    def attack_mode_4(self):
        pass

    def attack(self):
        super().attack()
        # there is a pause between each attack
        if self.shooting_current_cooldown_time <= 0 < self.energy:
            self.attack_modes[self.current_attack_mode]()
            self.attack_energy_charging_cooldown_time = self.ATTACK_ENERGY_CHARGING_MAX_TIME
            self.damagers = [damager for damager in self.damagers if damager.coo[0] < SCREEN_WIDTH]

    def update(self, dt: float):
        super().update(dt)
        [bullet.update(dt) for bullet in self.damagers]
        self.shooting_current_cooldown_time -= dt


class Bullet:
    """
        The Blaster weapon has the ability to fire different types of energy bullets.
        Each bullet has a different appearance, damage, speed, fire-rate, ...
        This class implements a base bullet, with the common functionalities.
            It is important to Add a static property to each Bullet-Child class that holds the frames for the bullet.
        Then the get_frame() method accesses this property to get the correct frame to display.
        This avoids having to load into memory the list of frames of each bullet when instantiated.
        Therefore, lowering memory usage and loading times.
            It is not possible to create the frames property in this parent-class because it would create a Bug where
            all bullets would have the same frames as the last Bullet type that has been instantiated.
    """

    def __init__(self, coo: (int, int)):
        # These coordinates are different from the coordinates of the player. They are already at pixel-value
        self.coo = coo
        self.current_frame = 0

    def get_frame(self):
        """
            This method should return the current bullet frame according to the static property that holds them.
            The property does not exist in the parent-class Bullet, and should instead be created for each of its children
        """
        raise Exception("Not implemented")

    def update(self, dt):
        raise Exception("Not implemented")

    def draw(self, screen):
        screen.blit(self.get_frame(), self.coo)


class BoltBullet(Bullet):
    """
        This type of bullet is not very fast and cost is relatively high, but damage dealt is worth it.
        Quality over Quantity
    """
    NAME = "Bolt"
    FRAMES = [grp.load_image(f"Battle/Weapons/Blaster/Bolt/{i}.png", scale=2) for i in range(5)]
    SPEED = 300          # Speed of the Bolt (pixel/Second)
    FRAME_SPEED = 25     # Time between each frame of the Bolt animation (Frame/Second)
    ENERGY_COST = 30     # Energy consumed by shooting a Bolt (Jolts)
    COOLDOWN_TIME = 3    # Time to wait before the next Bolt can be shot (Seconds)

    def __init__(self, coo: (int, int)):
        super().__init__(coo)

    def get_frame(self):
        """
            This method should return the current bullet frame according to the static property that holds them.
            The property does not exist in the parent-class Bullet, and should instead be created for each of its children
        """
        return self.FRAMES[int(self.current_frame)]

    def update(self, dt):
        self.current_frame = (self.current_frame +self.FRAME_SPEED*dt)%len(self.FRAMES)
        self.coo = (self.coo[0]+self.SPEED*dt, self.coo[1])


class ElectronBullet(Bullet):
    """
        This type of bullet is very fast and low-cost but also deals very little damage.
        It can be shot continuously up until the energy is depleted, creating a large number of bullets.
        Strength is in the Numbers.
    """
    NAME = "Electron"
    FRAMES = [grp.load_image(f"Battle/Weapons/Blaster/Electron/{i}.png", scale=2) for i in range(6)]
    SPEED = 1000          # Speed of the Bolt (pixel/Second)
    FRAME_SPEED = 20     # Time between each frame of the Bolt animation (Frame/Second)
    ENERGY_COST = 1      # Energy consumed by shooting a Bolt (Jolts)
    COOLDOWN_TIME = 0.06 # Time to wait before the next Bolt can be shot (Seconds)

    def __init__(self, coo: (int, int)):
        super().__init__(coo)

    def get_frame(self):
        """
            This method should return the current bullet frame according to the static property that holds them.
            The property does not exist in the parent-class Bullet, and should instead be created for each of its children
        """
        return self.FRAMES[int(self.current_frame)]

    def update(self, dt):
        self.current_frame = (self.current_frame +self.FRAME_SPEED*dt)%len(self.FRAMES)
        self.coo = (self.coo[0]+self.SPEED*dt, self.coo[1])


class QuantumBullet(Bullet):
    """
        This class represents a bullet, with a medium degree of damage, that switches rows randomly during its course.
    """
    NAME = "Quantum"
    FRAMES = [grp.load_image(f"Battle/Weapons/Blaster/Quantum/{i}.png", scale=2) for i in range(7)]
    SPEED = 100          # Speed of the Bolt (pixel/Second)
    FRAME_SPEED = 10     # Time between each frame of the Bolt animation (Frame/Second)
    ENERGY_COST = 20      # Energy consumed by shooting a Bolt (Jolts)
    COOLDOWN_TIME = 4 # Time to wait before the next Bolt can be shot (Seconds)

    def __init__(self, coo: (int, int)):
        super().__init__(coo)

    def get_frame(self):
        """
            This method should return the current bullet frame according to the static property that holds them.
            The property does not exist in the parent-class Bullet, and should instead be created for each of its children
        """
        return self.FRAMES[int(self.current_frame)]

    def update(self, dt):
        self.current_frame = self.current_frame +self.FRAME_SPEED*dt
        if self.current_frame >= len(self.FRAMES)-1:
            # The Quantum bullet can choose to switch to one of the 4 Rows (y = 0, 1, 2. 3)
            self.coo = (self.coo[0]+self.SPEED*dt, randint(0, 3)*-100+550)
            self.current_frame = 0
        else:
            self.coo = (self.coo[0]+self.SPEED*dt, self.coo[1])