from enum import Enum
from game_utils import *
import copy

#def checkPossible(x,y,grid):
#    
#    for i in range(-1,2):
#        for j in range(-1,2):
#            if(validate_space((x+i)%size, (y+j)%size, init_grid, x, y) == "safe"):
#                return True
#    return False

### Our first find_opp_place is a naive strategy, that might work (badly) for small boards if it actually isn't too slow

class Side(Enum):
    YOU = 0
    OPP = 1

you = "!"
opp = "@"

def simulate_move(x,y,grid,side,turn,oldx,oldy):
    if side == Side.YOU:
        if not checkPossible(x,y,grid):
            return 1 # Opp wins!
        if validate_space(x,y,grid,oldx,oldy) == "safe":
            grid[x][y][0][0] = you
            grid[x][y][0][1] = turn
        elif validate_space(x,y,grid,oldx,oldy) == "special":
            grid[x][y][1][0] = you
            grid[x][y][1][1] = turn
            return grid[x][y][0][0]
        else:
            return 0 # Invalid move
    elif side == Side.OPP:
        if not checkPossible(x,y,grid):
            return -1 # Opp loses. :'(
        if validate_space(x,y,grid,oldx,oldy) == "safe":
            grid[x][y][0][0] = opp
            grid[x][y][0][1] = turn
        elif validate_space(x,y,grid,oldx,oldy) == "special":
            grid[x][y][1][0] = opp
            grid[x][y][1][1] = turn
            return grid[x][y][0][0]

        else:
            return 0 # Invalid move

    else:
        log_print("THIS SHOULD NEVER HAPPEN")
        

def handle_specials_sim(grid):
    pass

def find_place(x,y,grid,youx,youy,turn,is_opp):
    size = len(grid)
    newgrid = copy.deepcopy(grid)
    return_val = [0,0,0] # First 2 params are the best x and y, and the 3rd parameter is the "goodness", which is "WIN" if it is a forced win for the current player, and "LOSE" if it is a forced loss for the current player, and otherwise a number equal to the number of continuations winning for the current player, minus the number of continuations losing for the current player.
    poses = [[[0] for j in range(3)] for i in range(3)]
    for i in range(-1,2):
        for j in range(-1,2):
            #poses[i+1][j+1]
            if is_opp:
                val = simulate_move((x+i)%size,(y+j)%size,newgrid,Side.OPP,turn,x,y)
            else:
                val = simulate_move((x+i)%size,(y+j)%size,newgrid,Side.YOU,turn,x,y)
            if val == 1:#We can immediately force-win with this move and need not check further
                return [(x+i)%size, (y+j)%size, "WIN"]
            if val == -1:#This move is an instant loss, so we have a new continuation 
                pass # TODO: FINISH THIS WHOLE FUNCTION
            if val == None:
                for k in range(-1,2):
                    find_place(x,y,grid,youx,youy,turn,not is_opp)
