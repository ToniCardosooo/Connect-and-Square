from typing import *
from copy import deepcopy
import numpy as np
from classes import Config
from drawingFuncs import *
from gameplayFuncs import *


# random play algorithm
def random_play(config : Config):
    
    first_dot_coord = (config.grid_size-1, config.grid_size-1)

    while (first_dot_coord == (config.grid_size-1, config.grid_size-1)):
        rand_j = np.random.randint(0, config.grid_size)
        rand_i = np.random.randint(0, config.grid_size)
        first_dot_coord = (rand_j, rand_i)

    vectors = [(1,0), (0,1)]
    # if the dot is in the last collumn
    if (rand_j == config.grid_size-1):
        vectors.remove((1,0))
    # if the dot is in the last row
    elif (rand_i == config.grid_size-1):
        vectors.remove((0,1))
    
    rand_index = np.random.randint(0,len(vectors))
    rand_vec = vectors[rand_index]
    
    first_dot_coord : Tuple[int, int] = (rand_j, rand_i)
    second_dot_coord : Tuple[int, int] = (rand_j + rand_vec[0], rand_i + rand_vec[1])
    
    return first_dot_coord, second_dot_coord



# greedy AI algorithm
def greedy(grid, config : Config):

    grid_original = deepcopy(grid)

    best_play = (0, tuple(), tuple(), Dot(), Dot()) # 0: num squares made | 1: first dot coord | 2: second dot coord | 3: first dot object | 4: second dot object
    
    for i in range(config.grid_size):
        for j in range(config.grid_size):
            
            grid_copy = deepcopy(grid_original)

            vectors = [(1,0), (0,1)]
            # if the dot is in the last collumn
            if (j == config.grid_size-1):
                vectors.remove((1,0))
            # if the dot is in the last row
            if (i == config.grid_size-1):
                vectors.remove((0,1))

            # possible directions
            for vec in vectors:
                first_dot : Dot = grid_copy[i][j]
                f_dot_coord = (j, i)

                # cant play over already drawn lines
                if (lineIsEmpty(grid_original, f_dot_coord, (j+vec[0], i+vec[1]))):

                    second_dot : Dot = grid_copy[i+vec[1]][j+vec[0]]
                    s_dot_coord = (j+vec[0], i+vec[1])

                    diff_0 = f_dot_coord[0] - s_dot_coord[0]
                    diff_1 = f_dot_coord[1] - s_dot_coord[1]

                    updateDotState(first_dot, diff_0, diff_1)
                    updateDotState(second_dot, diff_0, diff_1)

                    # AI will choose the first move that makes the biggest amount of squares
                    points = playerMadeSquare(grid_copy, f_dot_coord, s_dot_coord)
                    if (points > best_play[0]):
                        print("square "*points)
                        best_play = (points, f_dot_coord, s_dot_coord, first_dot, second_dot)

                    removeUpdate(first_dot, diff_0, diff_1)
                    removeUpdate(second_dot, diff_0, diff_1)         
                    
    
    # if all moves don't lead into a square being formed, select a random play
    if (best_play[0] == 0):

        grid_copy = deepcopy(grid)

        first_dot_coord, second_dot_coord = random_play(config)

        while (not lineIsEmpty(grid_copy, first_dot_coord, second_dot_coord)):
            first_dot_coord, second_dot_coord = random_play(config)

        first_dot : Dot = grid_copy[first_dot_coord[1]][first_dot_coord[0]]
        second_dot : Dot = grid_copy[second_dot_coord[1]][second_dot_coord[0]]

        best_play = (0, first_dot_coord, second_dot_coord, first_dot, second_dot)


    # return the AI score, both dots coordinates, and the grid with the correspondent dots un-updated
    return best_play[0], best_play[1], best_play[2], best_play[3], best_play[4]
        #     score      f_dot_coord   s_dot_coord   first_dot     second_dot
