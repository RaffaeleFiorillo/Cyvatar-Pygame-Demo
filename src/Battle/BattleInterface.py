import pygame
from pygame import Surface
from src.BaseInterface import BaseInterface
from .Controller import Controller
from src.utils import graphics as grp
from src import app_config as conf
import src.Battle.Warriors as Warriors


class BattleInterface(BaseInterface):
    """
    This class represents the events of a battle between the player and a set of enemies.
    """

    # This is the link to this interface. No Interface can have the same link.
    link: str = "Battle"

    def __init__(self, screen: Surface):
        super().__init__(screen)
        self.background = grp.load_image("Battle/Fields/GrassField/Field.png", (conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT))
        self.front_base = grp.load_image("Battle/Fields/GrassField/Base.png", (conf.SCREEN_WIDTH, 100))
        self.player = Warriors.BlasterPlayer()
        self.controller = Controller()
        self.clock = pygame.time.Clock()

    @staticmethod
    def display(screen: Surface):
        interface = BattleInterface(screen)
        next_link = interface.start()
        return next_link

    def refresh(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        self.screen.blit(self.front_base, (0, self.screen.get_height()-self.front_base.get_height()))
        pygame.display.update()

    def manage_events(self) -> bool:  # returns action to take based on input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        pressed_buttons = self.controller.get_pressed()
        self.player.act(pressed_buttons)
        return True

    def start(self) -> str:
        """
        Starts the interface process. This process ends when the link for the next interface is returned.

        :return: The link for the interface that should be shown next.
        """
        ongoing_battle = True
        while ongoing_battle:
            ongoing_battle = self.manage_events()
            dt = self.clock.tick(60)/1000
            self.player.update(dt)
            self.refresh()

        return "open_world"  # returns to the normal game