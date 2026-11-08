from src.Battle.BattleInterface import BattleInterface
from .ExitInterface import Exit
from .MainMenuInterface import MainMenu
from .HelpInterface import Help

STARTING_LINK = BattleInterface.link  # the link to the interface chosen to be the starting point of the App
ENDING_LINK = Exit.link
INTERFACE_LIST = [BattleInterface, Exit]
