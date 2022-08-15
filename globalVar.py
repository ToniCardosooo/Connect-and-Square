import pygame

# display height and width as global variables
DISPLAY_HEIGHT = 1000
DISPLAY_WIDTH = 1000

GRID_OFFSET = 150
FONT_SIZE = GRID_OFFSET//3

# colors in RBG tuples
WHITE = (255, 255, 255)
GREY_LIGHT = (211, 211, 211)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLUE_LIGHT = (173, 216, 230)
ORANGE = (255, 165, 0)
ORANGE_LIGHT = (254, 216, 177)
PINK = (205, 103, 184)
PINK_SOFT = (244, 194, 194)
PURPLE = (112, 12, 179)
PURPLE_SOFT = (175, 143, 233)

# different graphic styles for the game
default_player_color = [BLUE, ORANGE]
default_square_color = [BLUE_LIGHT, ORANGE_LIGHT]

melody_and_kuromi_player = [PINK, PURPLE]
melody_and_kuromi_square = [PINK_SOFT, PURPLE_SOFT]

player_color = [default_player_color, melody_and_kuromi_player]
square_color = [default_square_color, melody_and_kuromi_square]

# images 
MELODY_IMAGE = pygame.image.load("melody.png")
KUROMI_IMAGE = pygame.image.load("kuromi.png")

# processing / resizing images
