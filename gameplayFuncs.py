from typing import *
import pygame
from classes import Dot
from globalVar import *


# creates grid of the game
def createGrid(size: int):
    grid = list()
    for _ in range(size):
        row = list()
        for _ in range(size):
            row.append(Dot())
        grid.append(row)
    return grid


# gives the grid's indices of the dot selected on screen
def getSelectedDot(grid_length: int):
    # get the indices
    click = pygame.mouse.get_pos()   
    j = int((click[0]-GRID_OFFSET)*grid_length/(DISPLAY_WIDTH - 2*GRID_OFFSET))
    i = int((click[1]-GRID_OFFSET)*grid_length/(DISPLAY_HEIGHT - 2*GRID_OFFSET))

    # correct the click placement if it was out of range
    if (i >= grid_length):
        i = grid_length-1
    elif (i < 0):
        i = 0
    if (j >= grid_length):
        j = grid_length-1
    elif (j < 0):
        j = 0
    
    coord = (j,i) # coord[0] == j && coord[1] == i
    return coord


def switch_player(player_id):
    return (player_id + 1)%2


# update dot's line occupance
def updateDotState(dot: Dot, diff_0: int, diff_1: int):
    if (diff_0 == -1):
        dot.right_line = True
    else:
        dot.left_line = True

    if (diff_1 == -1):
        dot.lower_line = True
    else:
        dot.upper_line = True


# check if player is not drawing over an already existing line
def lineIsEmpty(grid, dotA_coord, dotB_coord) -> bool:
    diff_0 = dotA_coord[0] - dotB_coord[0] # -1 --> dotA is on the left || 1 --> dotA is on the right
    diff_1 = dotA_coord[1] - dotB_coord[1] # -1 --> dotA is above || 1 --> dotA is below

    if (abs(diff_0) == 1 and diff_1 == 0):
        if (diff_0 == -1 and grid[dotA_coord[1]][dotA_coord[0]].right_line == True and grid[dotB_coord[1]][dotB_coord[0]].left_line == True):
            return False
        elif (diff_0 == 1 and grid[dotA_coord[1]][dotA_coord[0]].left_line == True and grid[dotB_coord[1]][dotB_coord[0]].right_line == True):
            return False
    
    elif (abs(diff_1) == 1 and diff_0 == 0):
        if (diff_1 == -1 and grid[dotA_coord[1]][dotA_coord[0]].lower_line == True and grid[dotB_coord[1]][dotB_coord[0]].upper_line == True):
            return False
        elif (diff_1 == 1 and grid[dotA_coord[1]][dotA_coord[0]].upper_line == True and grid[dotB_coord[1]][dotB_coord[0]].lower_line == True):
            return False
    
    return True


# check if the player has made a square
def playerMadeSquare(grid, first_dot_coord, second_dot_coord) -> int:

    '''
    Idea:
    Through both dots the user chose, we can determine if it was made a vertical or horizontal line.
    In case a vertical line was made, we just need to for both dots at the left or right of each dot we already have.
    Same goes for the horizontal line case, with the above and below dots of those we have.

    As we're getting our new two dots, we'll check to see if they are connected to the existing ones.
    If they are not, check the dots of the side, if those aren't too, no square was made.
    In case one of the directions is, check if the new dots are connected. If they aren't, go to the previous step and check the other side. If they are, there's a square.
    '''

    num_squares_made = 0

    dotA: Dot = grid[first_dot_coord[1]][first_dot_coord[0]] # first dot selected
    dotB: Dot = grid[second_dot_coord[1]][second_dot_coord[0]] # second dot selected

    diff_0 = first_dot_coord[0] - second_dot_coord[0] # -1 --> dotA is on the left || 1 --> dotA is on the right
    diff_1 = first_dot_coord[1] - second_dot_coord[1] # -1 --> dotA is above || 1 --> dotA is below

    # horizontal line
    if (abs(diff_0) == 1 and diff_1 == 0):

        # the line doesnt belong to the first row
        if (first_dot_coord[1] != 0):
            dotC: Dot = grid[first_dot_coord[1]-1][first_dot_coord[0]] # dot right above the first selected
            dotD: Dot = grid[second_dot_coord[1]-1][second_dot_coord[0]] # dot right above the second selected
            
            # check if the new dots are connect to the existing ones
            if ((dotA.upper_line == True and dotC.lower_line == True) and (dotB.upper_line == True and dotD.lower_line == True)):

                # check if the new dots are connected to each other
                if (diff_0 == -1 and (dotC.right_line == True and dotD.left_line == True)):
                    num_squares_made += 1
                    dotA.square_pos.append((1,0))
                elif (diff_0 == 1 and (dotC.left_line == True and dotD.right_line == True)):
                    num_squares_made += 1
                    dotA.square_pos.append((1,1))
            
        # the line doesnt belong to the last row
        if (first_dot_coord[1] != len(grid)-1):
            dotC: Dot = grid[first_dot_coord[1]+1][first_dot_coord[0]] # dot right below the first selected
            dotD: Dot = grid[second_dot_coord[1]+1][second_dot_coord[0]] # dot right below the second selected
            
            # check if the new dots are connect to the existing ones
            if ((dotA.lower_line == True and dotC.upper_line == True) and (dotB.lower_line == True and dotD.upper_line == True)):

                # check if the new dots are connected to each other
                if (diff_0 == -1 and (dotC.right_line == True and dotD.left_line == True)):
                    num_squares_made += 1
                    dotA.square_pos.append((0,0))
                elif (diff_0 == 1 and (dotC.left_line == True and dotD.right_line == True)):
                    num_squares_made += 1
                    dotA.square_pos.append((0,1))
    
    # vertical line
    elif (abs(diff_1) == 1 and diff_0 == 0):

        # the line doesnt belong to the first collumn
        if (first_dot_coord[0] != 0):
            dotC: Dot = grid[first_dot_coord[1]][first_dot_coord[0]-1] # dot on the left to the first selected
            dotD: Dot = grid[second_dot_coord[1]][second_dot_coord[0]-1] # dot on the left to the second selected
            
            # check if the new dots are connect to the existing ones
            if ((dotA.left_line == True and dotC.right_line == True) and (dotB.left_line == True and dotD.right_line == True)):

                # check if the new dots are connected to each other
                if (diff_1 == -1 and (dotC.lower_line == True and dotD.upper_line == True)):
                    num_squares_made += 1
                    dotA.square_pos.append((0,1))
                elif (diff_1 == 1 and (dotC.upper_line == True and dotD.lower_line == True)):
                    num_squares_made += 1
                    dotA.square_pos.append((1,1))
            
        # the line doesnt belong to the last collumn
        if (first_dot_coord[0] != len(grid)-1):
            dotC: Dot = grid[first_dot_coord[1]][first_dot_coord[0]+1] # dot on the right to the first selected
            dotD: Dot = grid[second_dot_coord[1]][second_dot_coord[0]+1] # dot on the right to the second selected
            
            # check if the new dots are connect to the existing ones
            if ((dotA.right_line == True and dotC.left_line == True) and (dotB.right_line == True and dotD.left_line == True)):

                # check if the new dots are connected to each other
                if (diff_1 == -1 and (dotC.lower_line == True and dotD.upper_line == True)):
                    num_squares_made += 1
                    dotA.square_pos.append((0,0))
                elif (diff_1 == 1 and (dotC.upper_line == True and dotD.lower_line == True)):
                    num_squares_made += 1
                    dotA.square_pos.append((1,0))

    return num_squares_made
