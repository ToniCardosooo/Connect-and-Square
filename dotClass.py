from typing import *

class Dot:
    def __init__(self, upper = False, lower = False, left = False, right = False) -> None:
        self.upper_line = upper
        self.lower_line = lower
        self.left_line = left
        self.right_line = right
        # (0,0) == top left | (0,1) == top right | (1,0) == bottom left | (1,1) == bottom right
        # once a square is confirmed to exist, attribute the corresponding tupple to the first dot selected
        self.square_pos: list[Tuple[int, int]] = []
