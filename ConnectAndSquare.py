from typing import *
import time
import pygame
from sys import exit
from classes import Config
from drawingFuncs import *
from gameplayFuncs import *
from playerAI import *

# initialize configurations
cfg = Config()
cfg.askGameMode()
cfg.askStyle()
cfg.askGridSize()


# initialize grid
grid = createGrid(cfg.grid_size)


# main
def main():
    running = True
    click_state = False
    player_id = 0
    player_score = [0,0]

    pygame.init()
    screen = setScreen()
    drawGrid(cfg.grid_size, screen)

    run_once = True
    while running:
        events = pygame.event.get()
        for event in events:
            
            # just to initialize the score board
            # without stoping it, it would be drawing infinitely times until the program closes
            if (run_once):
                displayPlayerScores(cfg.grid_size, screen, player_score, cfg)
                run_once = False

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # select the first dot
            if (event.type == pygame.MOUSEBUTTONDOWN and click_state == False and (cfg.gamemode == 0 or (cfg.gamemode == 1 and player_id == 0))):
                first_dot_coord = getSelectedDot(cfg.grid_size)
                drawSelectedDot(cfg.grid_size, screen, first_dot_coord, player_id, cfg)
                click_state = True

            # select the second dot
            elif (event.type == pygame.MOUSEBUTTONDOWN and click_state == True and (cfg.gamemode == 0 or (cfg.gamemode == 1 and player_id == 0))):

                second_dot_coord = getSelectedDot(cfg.grid_size)
                diff_0 = first_dot_coord[0] - second_dot_coord[0]
                diff_1 = first_dot_coord[1] - second_dot_coord[1]

                # check if the player is clicking on a different dot or not playing diagonaly
                if ((abs(diff_0) == 1 or abs(diff_1) == 1) and (abs(diff_0) ^ abs(diff_1) == True)): # ^ is the XOR bitwise operator
                    
                    # check if the player is not choosing a pair of dots already connected with a line
                    if lineIsEmpty(grid, first_dot_coord, second_dot_coord):
                        # if there's no line connecting the dots, update the correspondent attributes of the dots to make them connected and draw the line
                        updateDotState(grid[first_dot_coord[1]][first_dot_coord[0]], diff_0, diff_1)
                        updateDotState(grid[second_dot_coord[1]][second_dot_coord[0]], -diff_0, -diff_1)
                        drawLine(first_dot_coord, second_dot_coord, cfg.grid_size, screen, player_id, cfg)

                        # check if the player made / closed a square 
                        # if so, draw it and update the score
                        points = playerMadeSquare(grid, first_dot_coord, second_dot_coord)
                        if (points > 0):
                            player_score[player_id] += points
                            drawSquares(grid, screen, first_dot_coord, player_id, cfg)
                            displayPlayerScores(cfg.grid_size, screen, player_score, cfg)

                        if (points == 0):
                            player_id = switch_player(player_id)
                            drawSingleDot(cfg.grid_size, screen, first_dot_coord)
                            drawSingleDot(cfg.grid_size, screen, second_dot_coord)
                    else:
                        drawSingleDot(cfg.grid_size, screen, first_dot_coord)
                        print("That line is already occupied!\nPlay again!")
                    click_state = False
                
                # played on the same Dot
                elif (abs(diff_0) == 0 and abs(diff_1) == 0):
                    drawSingleDot(cfg.grid_size, screen, first_dot_coord)
                    print("You chose the same Dot!\nPlay again!")
                    click_state = False

                # played diagonaly
                elif (abs(diff_0) ^ abs(diff_1) == False):
                    drawSingleDot(cfg.grid_size, screen, first_dot_coord)
                    print("You can't make diagonal lines!\nPlay again!")
                    click_state = False


            # exclusive to the 'Human vs AI' gamemode: plays the AI turn
            elif (cfg.gamemode == 1 and player_id == 1):

                # to give some "thinking time" to the AI player
                time.sleep(1.0)

                # get AI play based on the algorithm
                points_AI, first_dot_coord, second_dot_coord, first_dot, second_dot = greedy(grid, cfg)

                # update the dots
                diff_0 = first_dot_coord[0] - second_dot_coord[0]
                diff_1 = first_dot_coord[1] - second_dot_coord[1]
                updateDotState(first_dot, diff_0, diff_1)
                updateDotState(second_dot, -diff_0, -diff_1)

                # apply the new states of the dots
                mergeDots(grid[first_dot_coord[1]][first_dot_coord[0]], first_dot)
                mergeDots(grid[second_dot_coord[1]][second_dot_coord[0]], second_dot)

                # display the AI move                
                drawLine(first_dot_coord, second_dot_coord, cfg.grid_size, screen, player_id, cfg)
                drawSingleDot(cfg.grid_size, screen, first_dot_coord)
                drawSingleDot(cfg.grid_size, screen, second_dot_coord)

                # check if the AI made / closed a square 
                # if so, draw it and update the score
                if (points_AI > 0):
                    player_score[player_id] += points_AI
                    drawSquares(grid, screen, first_dot_coord, player_id, cfg)
                    displayPlayerScores(cfg.grid_size, screen, player_score, cfg)

                elif (points_AI == 0):
                    player_id = switch_player(player_id)
                    

            # check if the game ended
            if player_score[0] + player_score[1] == (cfg.grid_size-1)**2:
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