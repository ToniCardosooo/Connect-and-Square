import pygame
from typing import *
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
    x_init, y_init = GRID_OFFSET, GRID_OFFSET # the first dot is draw at the (GRID_OFFSET, GRID_OFFSET) pixel
    x, y = x_init, y_init

    num_dots = grid_length*grid_length

    while (num_dots > 0):
        
        pygame.draw.circle(screen, BLACK, (x,y), (DISPLAY_HEIGHT - 2*GRID_OFFSET) / (4*grid_length))
        pygame.draw.circle(screen, WHITE, (x,y), (DISPLAY_HEIGHT - 2*GRID_OFFSET) / (6*grid_length))

        num_dots -= 1

        if (num_dots % grid_length == 0):
            x = x_init
            y += (DISPLAY_HEIGHT - 2*GRID_OFFSET) / (grid_length-1) # vertical position change
        else:
            x += (DISPLAY_WIDTH - 2*GRID_OFFSET) / (grid_length-1) # horizontal position change
        

# display on screen which Dot got selected
def drawSelectedDot(grid_length, screen, dot_coord, player_id, style_id):
    x = GRID_OFFSET + dot_coord[0] * ((DISPLAY_WIDTH - 2*GRID_OFFSET) / (grid_length-1))
    y = GRID_OFFSET + dot_coord[1] * ((DISPLAY_HEIGHT - 2*GRID_OFFSET) / (grid_length-1))
    pygame.draw.circle(screen, player_color[style_id][player_id], (x,y), (DISPLAY_HEIGHT - 2*GRID_OFFSET) / (4*grid_length))
    pygame.draw.circle(screen, WHITE, (x,y), (DISPLAY_HEIGHT - 2*GRID_OFFSET) / (6*grid_length))


# display the line formed between two selected dots
def drawLine(first_dot_coord, second_dot_cood, grid_lenght, screen, player_id, style_id):
    x_init = GRID_OFFSET + first_dot_coord[0] * ((DISPLAY_WIDTH - 2*GRID_OFFSET) / (grid_lenght-1))
    y_init = GRID_OFFSET + first_dot_coord[1] * ((DISPLAY_HEIGHT - 2*GRID_OFFSET) / (grid_lenght-1))
    pos_init = (x_init, y_init)

    x_end = GRID_OFFSET + second_dot_cood[0] * ((DISPLAY_WIDTH - 2*GRID_OFFSET) / (grid_lenght-1))
    y_end = GRID_OFFSET + second_dot_cood[1] * ((DISPLAY_HEIGHT - 2*GRID_OFFSET) / (grid_lenght-1))
    pos_end = (x_end, y_end)

    pygame.draw.line(screen, player_color[style_id][player_id], pos_init, pos_end, 5) 


# display the square(s) made by the user
def drawSquares(grid, screen, first_dot_coord, player_id, style_id):
    dot = grid[first_dot_coord[1]][first_dot_coord[0]]

    while len(dot.square_pos) > 0:
        vec = dot.square_pos.pop(0)

        x = GRID_OFFSET + (first_dot_coord[0] - vec[1]) * ((DISPLAY_WIDTH - 2*GRID_OFFSET) / (len(grid)-1))
        y = GRID_OFFSET + (first_dot_coord[1] - vec[0]) * ((DISPLAY_HEIGHT - 2*GRID_OFFSET) / (len(grid)-1))
        lenght = (DISPLAY_WIDTH - 2*GRID_OFFSET) / (len(grid)-1)

        pygame.draw.rect(screen, square_color[style_id][player_id], (x, y, lenght, lenght))

        # if style == melody and kuromy, display their face on top of the squares
        if (style_id == 1):
            image = MELODY_IMAGE if (player_id == 0) else KUROMI_IMAGE
            image = pygame.transform.scale(image, (lenght, lenght))
            screen.blit(image, (x,y))


# display the current score of the players
def displayPlayerScores(grid_length, screen, score_list: List[int], style_id: int):
    name_p0 = "Melody: " if style_id == 1 else "Player 1: "
    name_p1 = "Kuromi: " if style_id == 1 else "Player 2: "

    font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)

    score_p0 = font.render(name_p0 + str(score_list[0]), True, player_color[style_id][0])
    score_p1 = font.render(name_p1 + str(score_list[1]), True, player_color[style_id][1])

    text_rect_p0 = score_p0.get_rect()
    text_rect_p0.center = (DISPLAY_WIDTH//4 + FONT_SIZE , GRID_OFFSET//2) if (style_id == 1) else (DISPLAY_WIDTH//4, GRID_OFFSET//2)
    text_rect_p1 = score_p1.get_rect()
    text_rect_p1.center = (3*(DISPLAY_WIDTH//4) + FONT_SIZE , GRID_OFFSET//2) if (style_id == 1) else (3*(DISPLAY_WIDTH)//4, GRID_OFFSET//2)

    radius_of_black_circle = (DISPLAY_HEIGHT - 2*GRID_OFFSET) / (4*grid_length)
    pygame.draw.rect(screen, GREY_LIGHT, (0, 0, DISPLAY_WIDTH, GRID_OFFSET - radius_of_black_circle))
    screen.blit(score_p0, text_rect_p0)
    screen.blit(score_p1, text_rect_p1)

    if (style_id == 1):
        melody = pygame.transform.scale(MELODY_IMAGE, (FONT_SIZE, FONT_SIZE))
        melody_rect = melody.get_rect()
        melody_rect.center = (text_rect_p0.bottomleft[0] - FONT_SIZE, text_rect_p0.centery)

        kuromi = pygame.transform.scale(KUROMI_IMAGE, (FONT_SIZE, FONT_SIZE))
        kuromi_rect = kuromi.get_rect()
        kuromi_rect.center = (text_rect_p1.bottomleft[0] - FONT_SIZE, text_rect_p1.centery)

        screen.blit(melody, melody_rect)
        screen.blit(kuromi, kuromi_rect)