import pygame
from pygame import Surface
from src.utils import graphics as grp
from src.utils.common import lerp_colors
from .Player import Player


class AttackPlayer(Player):
    """
        This class expand upon the Player class enabling the usage of Attacks.
        This class also introduces the HUD of the player. In other words, it displays the Battle properties of the player.
        Battle properties: HP, Energy, Mana, SkillPoints, Tarok Deck, Active Item
    """

    def __init__(self, attack_pose_image_dir: str, w_name: str, w_level: int, am_names):
        super().__init__()
        # The following properties are very particular. It is important to give the specific values
        # for each AttackPlayer Child AFTER the super().__init__()
        self.weapon_coo = (0, 0)
        self.attack_modes : {0: callable} = {}

        # From here on, the properties are not required to be given a value outside this initialization

        self.weapon_name = w_name  # This MUST be the same as the weapon's images folder
        self.images["attack"] = grp.load_image(attack_pose_image_dir)
        self.weapon_level = w_level  # The blaster is an upgradable weapon, therefore it has levels starting at a base of 0
        self.weapon_image = grp.load_image(f"Battle/Weapons/{w_name}/{w_level}.png", scale=0.4)

        self.attack_modes_names = am_names
        # The Player unlocks the attack-modes through upgrading and shopping
        self.available_attack_modes = 2  # key for the last available attack mode. Zero means the player has only one attack mode
        self.damagers = []  # All entities created by using an attack (mode)
        self.current_attack_mode = 0     # The Selected attack mode. Attacking means using the associated attack mode
        self.already_switched_attack_mode = False  # Flag to know if the button L2 has not been released after switching
        self.display_weapon = False

        self.SHOOTING_TOTAL_COOLDOWN_TIME = 1
        self.shooting_current_cooldown_time = 0

        self.HUD = HUD(self)

    def unique_properties_initialization(self):
        raise Exception("""
        Must call this method after the super().__init__() of the ChildClass that Inherits from AttackPlayer.
        The following properties must be initialized:
            - self.weapon_coo
            - self.attack_modes
        """)

    def update_weapon_coo(self):
        raise Exception("Every Child of AttackPlayer must implement this method.")

    def add_hp(self, value: float):
        self.hp = min(self.MAX_HP, max(0, self.hp+value))
        self.HUD.update_hp()

    def add_energy(self, value: float):
        # Ignore any energy change while the depletion cooldown is active
        if self.energy_depletion_cooldown_time >= 0 < value:
            return
        old_energy = self.energy
        self.energy = min(self.MAX_ENERGY, max(0, self.energy + value))
        # If energy just reached 0, start the cooldown
        if old_energy > 0 >= self.energy:
            self.energy_depletion_cooldown_time = self.ENERGY_DEPLETION_TOTAL_COOLDOWN_TIME

        self.HUD.update_energy()

    def add_mana(self, value: float):
        self.mana = min(self.MAX_MANA, max(0, self.mana + value))
        self.HUD.update_mana()

    def manage_movement(self, pressed_buttons)-> bool:
        has_moved = super().manage_movement(pressed_buttons)
        if has_moved:
            self.update_weapon_coo()
        return has_moved

    def act(self, pressed_buttons: list) -> None:
        if "l2" in pressed_buttons:
            # Only Switch to the next attack mode if the L2 button has been released
            if not self.already_switched_attack_mode:
                self.current_attack_mode = (self.current_attack_mode+1)%(self.available_attack_modes+1)
                print(self.current_attack_mode)
                self.already_switched_attack_mode = True
        else:
            self.already_switched_attack_mode = False

        super().act(pressed_buttons)

    def draw(self, screen: Surface):
        self.HUD.draw(screen)
        super().draw(screen)
        if self.state == "attack":
            screen.blit(self.weapon_image, self.weapon_coo)
        [bullet.draw(screen) for bullet in self.damagers]


class HUD:
    """
        Class responsible for displaying the HUD of the player.
        It receives the player that uses it in order to have direct access to his information.
        It is important that, every time a player stat-property is altered, the right function to update the HUD is called.
        Ex: after adding a certain amount of mana to the *player.mana* property, you should call player.HUD.update_mana()
    """
    def __init__(self, player: AttackPlayer):
        self.player = player
        self.player_hud_image = grp.load_image('Battle/HUD/Player_HUD.png', (483, 137))
        self.taroks_hud_image = grp.load_image('Battle/HUD/Taroks_HUD.png', (374, 137))
        # HP
        self.hp_colors = {"max_life": (0, 255, 70),
                       "max_energy": (0, 255, 255),
                       "low": (255, 0, 0),
                       "mid_life": (230, 230, 100),
                       "mid_energy": (0, 0, 250),
                          }
        self.hp_color = self.hp_colors["max_life"]
        self.HP_BAR_MAX_SIZE = 355
        self.hp_rect = (115, 10, self.HP_BAR_MAX_SIZE, 15)
        # Energy
        self.energy_color = (0, 255, 255)
        self.ENERGY_BAR_MAX_SIZE = 330
        self.energy_rect = (110, 27, self.ENERGY_BAR_MAX_SIZE, 10)
        # Mana
        self.mana_frame = 0
        self.mana_barr_images = [grp.load_image(f"Battle/HUD/ManaBarr/{i}.png", (300, 100)) for i in range(18)]
        # Attack Modes
        # The HUD displays the currently active attack mode
        self.attack_modes: {int: pygame.Surface} = {}
        for i, mode_name in enumerate(self.player.attack_modes_names):
            image_dir = f"Battle/Weapons/{self.player.weapon_name}/{mode_name}/0.png"
            attack_mode_image = grp.load_image(image_dir, scale=2.5)
            self.attack_modes[i] = attack_mode_image

    def update_energy(self):
        energy_percentage = self.player.energy/ self.player.MAX_ENERGY
        self.energy_color = lerp_colors((0, 0, 255), (0, 255, 255), energy_percentage)
        self.energy_rect = (115, 27, energy_percentage*self.ENERGY_BAR_MAX_SIZE, 10)

    def update_mana(self):
        mana_percentage = self.player.mana/ self.player.MAX_MANA
        self.mana_frame = int(mana_percentage*17)

    def update_hp(self):
        hp_percentage = self.player.hp / self.player.MAX_HP
        if hp_percentage > 0.75:
            self.hp_color = self.hp_colors["max_hp"]
        elif  0.75 >= hp_percentage > 0.33:
            self.hp_color = self.hp_colors["mid_hp"]
        else:
            self.hp_color = self.hp_colors["low"]
        self.hp_rect = (115, 10, hp_percentage*self.HP_BAR_MAX_SIZE, 15)

    def draw(self, screen: Surface) -> None:
        pygame.draw.rect(screen, self.hp_color, self.hp_rect)
        pygame.draw.rect(screen, self.energy_color, self.energy_rect)
        screen.blit(self.player_hud_image, (0, 0))
        screen.blit(self.attack_modes[self.player.current_attack_mode], (22, 39))
        screen.blit(self.mana_barr_images[self.mana_frame], (110, 30))
        screen.blit(self.taroks_hud_image, (485, 0))