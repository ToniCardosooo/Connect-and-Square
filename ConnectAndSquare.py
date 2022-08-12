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



def main():
    running = True
    click_state = False
    player_id = 0
    player_score = [0,0]
    createGrid(grid)

    pygame.init()
    screen = setScreen()
    drawGrid(grid, screen)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if (event.type == pygame.MOUSEBUTTONDOWN and click_state == False):
                first_dot_coord = getSelectedDot(grid)
                drawSelectedDot(grid, screen, first_dot_coord, player_id)
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
                        drawLine(first_dot_coord, second_dot_coord, grid, screen, player_id)

                        points = playerMadeSquare(grid, first_dot_coord, second_dot_coord)
                        if (points > 0):
                            player_score[player_id] += points
                            drawSquares(grid, screen, first_dot_coord, player_id)

                        drawGrid(grid, screen)
                        if (points == 0):
                            player_id = switch_player(player_id)
                    else:
                        drawSingleDot(grid, screen, first_dot_coord)
                        print("That line is already occupied!\nPlay again!")
                    click_state = False
                
                # played on the same Dot
                elif (abs(diff_0) == 0 and abs(diff_1) == 0):
                    drawSingleDot(grid, screen, first_dot_coord)
                    print("You chose the same Dot!\nPlay again!")
                    click_state = False

                # played diagonaly
                elif (abs(diff_0) ^ abs(diff_1) == False):
                    drawSingleDot(grid, screen, first_dot_coord)
                    print("You can't make diagonal lines!\nPlay again!")
                    click_state = False
                

            if player_score[0] + player_score[1] == (len(grid)-1)**2:
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