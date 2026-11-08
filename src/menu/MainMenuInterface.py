from .BaseMenu import BaseMenu
from .MainMenuButton import MainMenuButton
from .ExitInterface import Exit
from .HelpInterface import Help


class MainMenu(BaseMenu):
    link = "MainMenu"

    def __init__(self, screen, direct, buttons):
        super().__init__(screen, direct, buttons)

    @staticmethod
    def display(screen) -> str:
        # audio.stop_all_sounds()
        # audio.play(change_menu_sound)
        buttons = BaseMenu.create_buttons(MainMenuButton, "menu/buttons/1", [ Help.link, Exit.link])
        m_m = MainMenu(screen, f"menu/interfaces/Main/main menu.png", buttons)

        next_link = m_m.start()
        return next_link
