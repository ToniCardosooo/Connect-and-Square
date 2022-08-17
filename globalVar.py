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

BLUE = (0, 0, 255)
BLUE_LIGHT = (173, 216, 230)
ORANGE = (255, 165, 0)
ORANGE_LIGHT = (254, 216, 177)

PINK = (205, 103, 184)
PINK_SOFT = (244, 194, 194)
PURPLE = (112, 12, 179)
PURPLE_SOFT = (175, 143, 233)

# images 
MELODY_IMAGE = pygame.image.load("melody.png")
KUROMI_IMAGE = pygame.image.load("kuromi.png")

# processing / resizing images
