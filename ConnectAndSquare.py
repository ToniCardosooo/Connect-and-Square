from typing import *
import pygame
from sys import exit
from dotClass import Dot
from drawingFuncs import *
from gameplayFuncs import *

# list that will hold the grid of dots
grid = list()

def createGrid(grid: List):
    size = int(input("What do you want the size of the grid to be? "))
    for _ in range(size):
        row = list()
        for _ in range(size):
            row.append(Dot())
        grid.append(row)
    return size


# asks user if it wants to play with the default style or with a melody_kuromi style
def askStyle():
    r = int(input("\n1) Default Style (Blue / Orange)\n2) 'Melody and Kuromi' Style\nWhat style do you want to play on? "))
    return r-1


def main():
    running = True
    click_state = False
    player_id = 0
    player_score = [0,0]
    style_id = askStyle()
    grid_length = createGrid(grid)

    pygame.init()
    screen = setScreen()
    drawGrid(grid_length, screen)

    while running:
        events = pygame.event.get()
        for event in events:

            displayPlayerScores(grid_length, screen, player_score, style_id)

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if (event.type == pygame.MOUSEBUTTONDOWN and click_state == False):
                first_dot_coord = getSelectedDot(grid)
                drawSelectedDot(grid_length, screen, first_dot_coord, player_id, style_id)
                click_state = True

            elif (event.type == pygame.MOUSEBUTTONDOWN and click_state == True):

                second_dot_coord = getSelectedDot(grid)
                diff_0 = first_dot_coord[0] - second_dot_coord[0]
                diff_1 = first_dot_coord[1] - second_dot_coord[1]

                # check if the player is clicking on a different dot or not playing diagonaly
                if ((abs(diff_0) == 1 or abs(diff_1) == 1) and (abs(diff_0) ^ abs(diff_1) == True)): # ^ is the XOR bitwise operator

                    if lineIsEmpty(grid, first_dot_coord, second_dot_coord):
                        updateDotState(grid[first_dot_coord[1]][first_dot_coord[0]], diff_0, diff_1)
                        updateDotState(grid[second_dot_coord[1]][second_dot_coord[0]], -diff_0, -diff_1)
                        drawLine(first_dot_coord, second_dot_coord, grid_length, screen, player_id, style_id)

                        points = playerMadeSquare(grid, first_dot_coord, second_dot_coord)
                        if (points > 0):
                            player_score[player_id] += points
                            drawSquares(grid, screen, first_dot_coord, player_id, style_id)

                        drawGrid(grid_length, screen)
                        if (points == 0):
                            player_id = switch_player(player_id)
                    else:
                        drawSingleDot(grid_length, screen, first_dot_coord)
                        print("That line is already occupied!\nPlay again!")
                    click_state = False
                
                # played on the same Dot
                elif (abs(diff_0) == 0 and abs(diff_1) == 0):
                    drawSingleDot(grid_length, screen, first_dot_coord)
                    print("You chose the same Dot!\nPlay again!")
                    click_state = False

                # played diagonaly
                elif (abs(diff_0) ^ abs(diff_1) == False):
                    drawSingleDot(grid_length, screen, first_dot_coord)
                    print("You can't make diagonal lines!\nPlay again!")
                    click_state = False
                

            if player_score[0] + player_score[1] == (grid_length-1)**2:
                running = False
                break
        pygame.display.update()
    
    if player_score[0] > player_score[1]:
        print(f"Player 1 has won with {player_score[0]} squares!")
    elif player_score[0] < player_score[1]:
        print(f"Player 2 has won with {player_score[1]} squares!")
    else:
        print("Tie!")



if __name__ == "__main__":
    main()