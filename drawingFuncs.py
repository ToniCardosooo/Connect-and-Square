import pygame
from typing import *
from classes import Dot, Config
from globalVar import *

# sets the game window
def setScreen():
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    screen.fill(GREY_LIGHT) # white background
    pygame.display.set_caption("Connect and Square!")
    return screen


# draw a single dot
def drawSingleDot(grid_length, screen, dot_coord):
    x = GRID_OFFSET + dot_coord[0] * ((DISPLAY_WIDTH - 2*GRID_OFFSET) / (grid_length-1))
    y = GRID_OFFSET + dot_coord[1] * ((DISPLAY_HEIGHT - 2*GRID_OFFSET) / (grid_length-1))
    pygame.draw.circle(screen, BLACK, (x,y), (DISPLAY_HEIGHT - 2*GRID_OFFSET) / (4*grid_length))
    pygame.draw.circle(screen, WHITE, (x,y), (DISPLAY_HEIGHT - 2*GRID_OFFSET) / (6*grid_length))


# draw the grid on the screen
def drawGrid(grid_length, screen):
    for i in range(grid_length):
        for j in range(grid_length):
            drawSingleDot(grid_length, screen, (j,i))


# display on screen which Dot got selected
def drawSelectedDot(grid_length, screen, dot_coord, player_id, cfg: Config):
    x = GRID_OFFSET + dot_coord[0] * ((DISPLAY_WIDTH - 2*GRID_OFFSET) / (grid_length-1))
    y = GRID_OFFSET + dot_coord[1] * ((DISPLAY_HEIGHT - 2*GRID_OFFSET) / (grid_length-1))
    pygame.draw.circle(screen, cfg.player_colors[player_id], (x,y), (DISPLAY_HEIGHT - 2*GRID_OFFSET) / (4*grid_length))
    pygame.draw.circle(screen, WHITE, (x,y), (DISPLAY_HEIGHT - 2*GRID_OFFSET) / (6*grid_length))


# display the line formed between two selected dots
def drawLine(first_dot_coord, second_dot_cood, grid_lenght, screen, player_id, cfg: Config):
    x_init = GRID_OFFSET + first_dot_coord[0] * ((DISPLAY_WIDTH - 2*GRID_OFFSET) / (grid_lenght-1))
    y_init = GRID_OFFSET + first_dot_coord[1] * ((DISPLAY_HEIGHT - 2*GRID_OFFSET) / (grid_lenght-1))
    pos_init = (x_init, y_init)

    x_end = GRID_OFFSET + second_dot_cood[0] * ((DISPLAY_WIDTH - 2*GRID_OFFSET) / (grid_lenght-1))
    y_end = GRID_OFFSET + second_dot_cood[1] * ((DISPLAY_HEIGHT - 2*GRID_OFFSET) / (grid_lenght-1))
    pos_end = (x_end, y_end)

    pygame.draw.line(screen, cfg.player_colors[player_id], pos_init, pos_end, 5) 


# re-draws the dots that are vertices of the square made
def drawSquareDots(grid, screen, grid_length, first_dot_coord, first_dot_square_pos):    
    
    second_dot_coord, third_dot_coord, fourth_dot_coord = (0,0), (0,0), (0,0)

    # if first dot is top left
    if (first_dot_square_pos == (0,0)):
        second_dot_coord = (first_dot_coord[0] + 1, first_dot_coord[1]) # top right
        third_dot_coord = (first_dot_coord[0], first_dot_coord[1] + 1) # bottom left
        fourth_dot_coord = (first_dot_coord[0] + 1, first_dot_coord[1] + 1) # bottom right

    # if first dot is top right
    elif (first_dot_square_pos == (0,1)):
        second_dot_coord = (first_dot_coord[0] - 1, first_dot_coord[1]) # top left
        third_dot_coord = (first_dot_coord[0] - 1, first_dot_coord[1] + 1) # bottom left
        fourth_dot_coord = (first_dot_coord[0], first_dot_coord[1] + 1) # bottom right

    # if first dot is bottom left
    elif (first_dot_square_pos == (1,0)):
        second_dot_coord = (first_dot_coord[0], first_dot_coord[1] - 1) # top left
        third_dot_coord = (first_dot_coord[0] + 1, first_dot_coord[1] - 1) # top right
        fourth_dot_coord = (first_dot_coord[0] + 1, first_dot_coord[1]) # bottom right

    # if first dot is bottom right
    elif (first_dot_square_pos == (1,1)):
        second_dot_coord = (first_dot_coord[0] - 1, first_dot_coord[1] - 1) # top left
        third_dot_coord = (first_dot_coord[0], first_dot_coord[1] - 1) # top right
        fourth_dot_coord = (first_dot_coord[0] - 1, first_dot_coord[1]) # bottom left

    drawSingleDot(grid_length, screen, first_dot_coord)
    drawSingleDot(grid_length, screen, second_dot_coord)
    drawSingleDot(grid_length, screen, third_dot_coord)
    drawSingleDot(grid_length, screen, fourth_dot_coord)


# display the square(s) made by the user
def drawSquares(grid, screen, first_dot_coord, player_id, cfg: Config):

    dot : Dot = grid[first_dot_coord[1]][first_dot_coord[0]]

    while len(dot.square_pos) > 0:

        first_dot_square_pos = dot.square_pos[0]

        vec = dot.square_pos.pop(0)

        x = GRID_OFFSET + (first_dot_coord[0] - vec[1]) * ((DISPLAY_WIDTH - 2*GRID_OFFSET) / (len(grid)-1))
        y = GRID_OFFSET + (first_dot_coord[1] - vec[0]) * ((DISPLAY_HEIGHT - 2*GRID_OFFSET) / (len(grid)-1))
        lenght = (DISPLAY_WIDTH - 2*GRID_OFFSET) / (len(grid)-1)

        pygame.draw.rect(screen, cfg.square_colors[player_id], (x, y, lenght, lenght))

        # if style == melody and kuromy, display their face on top of the squares
        if (cfg.style == 1):
            image = MELODY_IMAGE if (player_id == 0) else KUROMI_IMAGE
            image = pygame.transform.scale(image, (lenght, lenght))
            screen.blit(image, (x,y))

        # re-draw dots
        drawSquareDots(grid, screen, cfg.grid_size, first_dot_coord, first_dot_square_pos)



# display the current score of the players
def displayPlayerScores(grid_length, screen: pygame.Surface, score_list: List[int], cfg: Config):
    name_p0 = "Melody: " if cfg.style == 1 else "Player 1: "
    name_p1 = "Kuromi: " if cfg.style == 1 else "Player 2: "

    font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)

    score_p0 = font.render(name_p0 + str(score_list[0]), True, cfg.player_colors[0])
    score_p1 = font.render(name_p1 + str(score_list[1]), True, cfg.player_colors[1])

    text_rect_p0 = score_p0.get_rect()
    text_rect_p0.center = (DISPLAY_WIDTH//4 + FONT_SIZE , GRID_OFFSET//2) if (cfg.style == 1) else (DISPLAY_WIDTH//4, GRID_OFFSET//2)
    text_rect_p1 = score_p1.get_rect()
    text_rect_p1.center = (3*(DISPLAY_WIDTH//4) + FONT_SIZE , GRID_OFFSET//2) if (cfg.style == 1) else (3*(DISPLAY_WIDTH)//4, GRID_OFFSET//2)

    radius_of_black_circle = (DISPLAY_HEIGHT - 2*GRID_OFFSET) / (4*grid_length)
    pygame.draw.rect(screen, GREY_LIGHT, (0, 0, DISPLAY_WIDTH, GRID_OFFSET - radius_of_black_circle))
    screen.blit(score_p0, text_rect_p0)
    screen.blit(score_p1, text_rect_p1)

    if (cfg.style == 1):
        melody = pygame.transform.scale(MELODY_IMAGE, (1.5*FONT_SIZE, 1.5*FONT_SIZE))
        melody_rect = melody.get_rect()
        melody_rect.center = (text_rect_p0.bottomleft[0] - 1.5*FONT_SIZE, text_rect_p0.centery)

        kuromi = pygame.transform.scale(KUROMI_IMAGE, (1.5*FONT_SIZE, 1.5*FONT_SIZE))
        kuromi_rect = kuromi.get_rect()
        kuromi_rect.center = (text_rect_p1.bottomleft[0] - 1.5*FONT_SIZE, text_rect_p1.centery)

        screen.blit(melody, melody_rect)
        screen.blit(kuromi, kuromi_rect)