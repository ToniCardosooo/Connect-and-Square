from typing import *
from globalVar import *

class Dot:
    def __init__(self, upper = False, lower = False, left = False, right = False) -> None:
        self.upper_line : bool = upper
        self.lower_line : bool = lower
        self.left_line : bool = left
        self.right_line : bool = right

        # (0,0) == top left | (0,1) == top right | (1,0) == bottom left | (1,1) == bottom right
        # once a square is confirmed to exist, attribute the corresponding tupple to the first dot selected
        self.square_pos: list[Tuple[int, int]] = []
    
    def __eq__(self, other) -> bool:
        return (self.left_line == other.left_line and self.right_line == other.right_line and self.upper_line == other.upper_line and self.lower_line == other.lower_line)


class Config:
    def __init__(self):
        self.grid_size : int = None
        self.gamemode : int = 0 # 0: Human vs Human | 1: Human vs PC
        self.style = None
        self.player_colors : Tuple[ Tuple[int, int, int] , Tuple[int, int, int] ] = None
        self.square_colors : Tuple[ Tuple[int, int, int] , Tuple[int, int, int] ] = None

    def askGameMode(self):
        self.gamemode = int(input("\n1) Human vs Human\n2) Human vs AI (greedy algorithm)\nWhich game mode do you want to play on? ")) - 1
    
    def askStyle(self):
        self.style = int(input("\n1) Default Style (Blue / Orange)\n2) 'Melody and Kuromi' Style\nWhich style do you want to play on? ")) - 1

        if (self.style == 0):
            self.player_colors = [BLUE, ORANGE, RED]
            self.square_colors = [BLUE_LIGHT, ORANGE_LIGHT]
        
        else:
            self.player_colors = [PINK, PURPLE, RED]
            self.square_colors = [PINK_SOFT, PURPLE_SOFT]
    
    def askGridSize(self):
        self.grid_size = int(input("\nWhat do you want the size of the grid to be? "))
    

class GameState:
    def __init__(self, current_game_score, current_game_grid):
        current_score : List = current_game_score
        current_grid = current_game_grid
    
    