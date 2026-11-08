import pygame
from pygame import Surface


class Warrior:
    """
    This class represents every character that can be placed in the battlefield
    """
    PLAYER_FIELD_RANGE = 3  # The player can only reach the tiles with x coordinates inferior to this range

    def __init__(self, x: int, y: int):
        self.x = x # x coordinate of the warrior on the grid
        self.y = y # y coordinate of the warrior on the grid

    def get_pixel_coordinates(self):
        raise Exception("Not implemented method")

    def draw(self, screen: Surface):
        raise Exception("Not implemented method")