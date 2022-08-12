import pygame
from gameplayFuncs import getSelectedDot

# display height and width as global variables
DISPLAY_HEIGHT = 1000
DISPLAY_WIDTH = 1000

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

player_color = [BLUE, ORANGE]
square_color = [BLUE_LIGHT, ORANGE_LIGHT]

# sets the game window
def setScreen():
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    screen.fill(GREY_LIGHT) # white background
    pygame.display.set_caption("Connect and Square!")
    return screen


# draw a single dot
def drawSingleDot(grid, screen, dot_coord):
    x = 100 + dot_coord[0] * ((DISPLAY_WIDTH - 2*100) / (len(grid)-1))
    y = 100 + dot_coord[1] * ((DISPLAY_HEIGHT - 2*100) / (len(grid)-1))
    pygame.draw.circle(screen, BLACK, (x,y), (DISPLAY_HEIGHT - 2*100) / (4*len(grid)))
    pygame.draw.circle(screen, WHITE, (x,y), (DISPLAY_HEIGHT - 2*100) / (6*len(grid)))



# draw the grid on the screen
def drawGrid(grid, screen):
    x_init, y_init = 100, 100 # the first dot is draw at the (100, 100) pixel
    x, y = x_init, y_init

    num_dots = len(grid)*len(grid)

    while (num_dots > 0):
        
        pygame.draw.circle(screen, BLACK, (x,y), (DISPLAY_HEIGHT - 2*100) / (4*len(grid)))
        pygame.draw.circle(screen, WHITE, (x,y), (DISPLAY_HEIGHT - 2*100) / (6*len(grid)))

        num_dots -= 1

        if (num_dots % len(grid) == 0):
            x = x_init
            y += (DISPLAY_HEIGHT - 2*100) / (len(grid)-1) # vertical position change
        else:
            x += (DISPLAY_WIDTH - 2*100) / (len(grid)-1) # horizontal position change
        

# display on screen which Dot got selected
def drawSelectedDot(grid, screen, dot_coord, player_id):
    x = 100 + dot_coord[0] * ((DISPLAY_WIDTH - 2*100) / (len(grid)-1))
    y = 100 + dot_coord[1] * ((DISPLAY_HEIGHT - 2*100) / (len(grid)-1))
    pygame.draw.circle(screen, player_color[player_id], (x,y), (DISPLAY_HEIGHT - 2*100) / (4*len(grid)))
    pygame.draw.circle(screen, WHITE, (x,y), (DISPLAY_HEIGHT - 2*100) / (6*len(grid)))


# display the line formed between two selected dots
def drawLine(first_dot_coord, second_dot_cood, grid, screen, player_id):
    x_init = 100 + first_dot_coord[0] * ((DISPLAY_WIDTH - 2*100) / (len(grid)-1))
    y_init = 100 + first_dot_coord[1] * ((DISPLAY_HEIGHT - 2*100) / (len(grid)-1))
    pos_init = (x_init, y_init)

    x_end = 100 + second_dot_cood[0] * ((DISPLAY_WIDTH - 2*100) / (len(grid)-1))
    y_end = 100 + second_dot_cood[1] * ((DISPLAY_HEIGHT - 2*100) / (len(grid)-1))
    pos_end = (x_end, y_end)

    pygame.draw.line(screen, player_color[player_id], pos_init, pos_end, 5) 


# display the square(s) made by the user
def drawSquares(grid, screen, first_dot_coord, player_id):
    dot = grid[first_dot_coord[1]][first_dot_coord[0]]

    while len(dot.square_pos) > 0:
        vec = dot.square_pos.pop(0)

        x = 100 + (first_dot_coord[0] - vec[1]) * ((DISPLAY_WIDTH - 2*100) / (len(grid)-1))
        y = 100 + (first_dot_coord[1] - vec[0]) * ((DISPLAY_HEIGHT - 2*100) / (len(grid)-1))
        lenght = (DISPLAY_WIDTH - 2*100) / (len(grid)-1)

        pygame.draw.rect(screen, square_color[player_id], (x, y, lenght, lenght))