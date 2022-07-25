from opp_strat import *
from game_utils import *

bots = False

def handle_special(x, y, grid):
    special = grid[x][y][0][0]
    if (special == "B"):
        if not bots:
            log_print("You hit a trampoline! Your opponent's turn is skipped and on your next turn, you get to bounce off of it in any direction (effectively, you get two turns in a row)")
        global special_flag_B
        special_flag_B = True
    if (special == "P"):
        if not bots:
            log_print("You hit a power pellet! For the next " + str(power_pellet_max_turns) + " turns, including this one, you get " + str(power_pellet_max_moves + 1) + " moves, instead of just one. Have fun! As a note, this doesn't stack but duration will increase.")
        global power_pellet_moves
        global power_pellet_turns
        power_pellet_turns += power_pellet_max_turns
        power_pellet_moves = power_pellet_max_moves


def handle_opp_specials(x, y, grid):
    special = grid[x][y][0][0]
    if (special == "B"):
        global special_flag_B_opp
        special_flag_B_opp = True
    if (special == "P"):
        global power_pellet_moves_opp
        global power_pellet_turns_opp
        power_pellet_turns_opp += power_pellet_max_turns
        power_pellet_moves_opp = power_pellet_max_moves



power_pellet_turns = 0
power_pellet_moves = 0
power_pellet_max_moves = 1
power_pellet_max_turns = 2
power_pellet_done = False

power_pellet_turns_opp = 0
power_pellet_moves_opp = 0
power_pellet_done_opp = False

special_flag_B = False

special_flag_B_opp = False

### GAME

os.system("clear")

name = log_input("Hi! Welcome to Multiplayer Snake! Please input your first initial. ")

try:
    name = name[0].lower()
    if name == " ":
        name = "d"
except:
    name = "d"

size = int(log_input("How big do you want your grids? "))

while True:
    power_pellet_turns = 0
    power_pellet_moves = 0
    power_pellet_max_moves = 1
    power_pellet_max_turns = 2
    power_pellet_done = False

    power_pellet_turns_opp = 0
    power_pellet_moves_opp = 0
    power_pellet_done_opp = False

    special_flag_B = False

    special_flag_B_opp = False


    bots = log_input("Would you like to play, or just watch bots play? (b = bots, anything else = you) ")

    if (bots.lower() == "b"):
        bots = True
    else:
        bots = False

    ### Set up pauseability via threading
    
    paused = False

    if bots:
        pass        

    ### TODO: Implement the above

    grid = startup(size, name)

    x = 0
    oldx = 0
    y = 0
    oldy = 0
    turncount = 0
    opponentx = size - 1
    opponenty = size - 1

    print_grid(grid)

    special_turn = False
    special_turn_opp = False


    will_cont_opp = False

    while True:
        turns(turncount)
        print_grid(grid)

        if(not special_flag_B_opp and (power_pellet_moves_opp == 0 or power_pellet_done_opp)):
            turncount += 1
            oldx = x
            oldy = y

        ### VALIDATE INPUT ###
            if not checkPossible(x, y, grid):
                print_grid(grid)
                log_print("Unfortunately, you lose! You lasted " + str(turncount) + " turns.")
                break


            if not bots:
                direct = log_input("Pick a direction to move in: (one or two of n/s/e/w) ").lower()
                if(len(direct) > 2): 
                    log_print("You must enter a valid direction!")
                    turncount -= 1
                    continue
                if (len(direct) == 2 and direct[0] == direct[1]):
                    log_print("You must enter up to two distinct directions!")
                    turncount -= 1
                    continue
                y = (oldy + ("e" in direct) - ("w" in direct)) % size
                x = (oldx - ("n" in direct) + ("s" in direct)) % size
                if(x == oldx and y == oldy):
                    log_print("You have entered an invalid direction.")
                    turncount -= 1
                    continue
                if(validate_space(x, y, grid, oldx, oldy) == "crossing"):
                    log_print("You can't cross over someone else's tail!")
                    x = oldx
                    y = oldy
                    turncount -= 1
                    continue
            else:
                xchange = random.randint(-1,1)
                ychange = random.randint(-1,1)
                x += xchange
                y += ychange
                x = x % size
                y = y % size
                if(xchange == 0 and ychange == 0):
                    turncount -= 1
                    continue
                if(validate_space(x, y, grid, oldx, oldy) == "crossing"):
                    x = oldx
                    y = oldy
                    turncount -= 1
                    continue

        ### MAKE MOVE ###

            if(checkspace(x,y,grid) == "safe"):
                grid[x][y][0][0] = name
                grid[x][y][0][1] = str(turncount)
            elif(checkspace(x,y,grid) == "special"):
                grid[x][y][1][0] = name
                grid[x][y][1][1] = str(turncount)
                handle_special(x, y, grid)
            else:
                if not bots:
                    log_print("You've moved into an occupied space; please try again.")
                x = oldx
                y = oldy
                turncount -= 1
                continue


        ### HANDLE SPECIALS ###
            
            special_turn = False #Not yet used

            will_cont = False
            if(special_flag_B):
                special_flag_B = False
                turncount -= 1
                will_cont = True
                special_turn = True
                continue
                
            if(not power_pellet_done):
                if(power_pellet_moves > 0):
                    power_pellet_moves -= 1
                    will_cont = True
                if(power_pellet_moves == 0 and power_pellet_turns > 0):
                    power_pellet_turns -= 1
                if (power_pellet_turns > 0 and power_pellet_moves == 0):
                    power_pellet_moves = power_pellet_max_moves
                    power_pellet_done = True
                if (will_cont):
                    special_turn = True
                    turncount -= 1
                    continue
            else:
                if not special_turn:
                    power_pellet_done = False
                
        else:
            pass
        will_cont_opp = False
        special_turn_opp = False
        if (special_flag_B_opp):
            special_turn_opp = True
        special_flag_B_opp = False
        if(not power_pellet_done_opp and not special_turn_opp):
            if(power_pellet_moves_opp > 0):
                power_pellet_moves_opp -= 1
            if(power_pellet_moves_opp == 0 and power_pellet_turns_opp > 0):
                power_pellet_turns_opp -= 1
            if (power_pellet_turns_opp > 0 and power_pellet_moves_opp == 0):
                power_pellet_moves_opp = power_pellet_max_moves
                power_pellet_done_opp = True
            if (will_cont_opp):
                special_turn_opp = True
        else:
            if not special_turn_opp:
                power_pellet_done_opp = False
        
        flag = False

        do_it = True
    
        print_grid(grid)
    
        #if bots:
        time.sleep(1)

        if not checkPossible(opponentx, opponenty, grid):
            do_it = False # Don't bother if I can't move anywhere

        canEscape = False
        for i in range(-1,2):
            for j in range(-1,2):
                if checkPossible((opponentx + i) % size, (opponenty + j) % size, grid):
                    canEscape = True

        #for i in range (1000): # Should be enough to be decently sure no move is possible if it fails, and it will usually break early
        while do_it: # should always break early
            oppxchange = random.randint(-1,1)
            oppychange = random.randint(-1,1)
            if not checkPossible((opponentx + oppxchange) % size, (opponenty + oppychange) % size, grid) and canEscape:
                continue # Basic checking where the opponent won't kill itself if it can possibly avoid it
            if validate_space((opponentx + oppxchange) % size, (opponenty + oppychange) % size, grid, opponentx, opponenty) == "crossing":
                continue
            elif validate_space((opponentx + oppxchange) % size, (opponenty + oppychange) % size, grid, opponentx, opponenty) == "safe":
                grid[(opponentx + oppxchange) % size][(opponenty + oppychange) % size][0][0] = "@"
                grid[(opponentx + oppxchange) % size][(opponenty + oppychange) % size][0][1] = str(turncount)
                opponentx = (opponentx + oppxchange) % size
                opponenty = (opponenty + oppychange) % size
                flag = True
                break
            elif validate_space((opponentx + oppxchange) % size, (opponenty + oppychange) % size, grid, opponentx, opponenty) == "special":
                opponentx = (opponentx + oppxchange) % size
                opponenty = (opponenty + oppychange) % size
                handle_opp_specials(opponentx, opponenty, grid)
                grid[opponentx][opponenty][1][0] = "@"
                grid[opponentx][opponenty][1][1] = str(turncount)
                flag = True
                break

        if not flag:
            print_grid(grid)
            log_print("You won! The opponent can't move. You won after: " + str(turncount) + " turns.")
            break
        
        print_grid(grid)
        if bots:
            time.sleep(1)
    a = log_input("Would you like to play again? (y/n) ")
    if (not (a.lower() == "y" or a.lower() == "yes")):
        log_print("Thanks for playing!")
        break
