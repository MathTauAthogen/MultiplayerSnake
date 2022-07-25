import os
import random
import sys
import time
import math
import threading

#### STARTUP

log = []

size = 0

startup = True

specials_list = [["B","184"], ["P","10"], ["S","18"]]
probs = [0.05,0.05,0.2]

screen_width = 211 # Accurate for my own fullscreen

turn = 0

myname = ""

def turns(count):
    global turn
    turn = count

def startup(the_size, name):
    global myname
    myname = name
    startup = False
    global size
    size = the_size

    #specials = [[1,1,"B"], [size - 2, size - 2, "B"], [2,2,"P"]]

    specials = []
    
    cutoffs = [sum(probs[:i]) for i in range(len(probs))]

    for i in range(size):
        for j in range(size):
            if i == j and (i == 0 or i == size - 1):
                continue
            else:
                which = random.random()
                for ind, k in enumerate(cutoffs):
                    if which <= k:
                        specials += [[i,j, specials_list[ind][0]]]
                        break
                        

    init_grid = [[[[" "," "],[" ", " "], [""], [""]] for j in range(size)] for i in range(size)]

    init_grid[0][0] = [[name, " "], [" ", " "], [""], [""]]

    init_grid[-1][-1] = [["@", " "], [" ", " "], [""], [""]]

    for i in specials:
        init_grid[i[0]][i[1]][0][0] = i[2] 

    return init_grid

#### LOGGING

def log_input(string):
    global log
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    if not startup:
        print_grid(init_grid)
    a = input(current_time + " " * 7 + string)
    log += [[current_time, string + a]]
    if len(log) > 10:
        log[:] = log[1:]
    return a

def log_print(string):
    #all_background = "208"
    #text_color = "46"
    #print("\033[48;5;"+ all_background +"m")

    global log
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    if not startup:
        print_grid(init_grid)
    print_string = current_time + " " * 7 + string

    #print_string += " " * (screen_width - len(print_string))
    #print("\033[38;5;" + text_color + "m" + print_string + "\033[38;5;0m")

    print(print_string)
    log += [[current_time, string]]
    if len(log) > 10:
        log[:] = log[1:]

def print_grid (grid):

    os.system("clear")
    
    height = len(grid)
    width = len(grid[0])
    all_background = "202";
    borders = "22";
    me = "210";
    opp = "226";
    turncolor = "171";
    print("\033[48;5;" + all_background + "m", end="")
    for i in range(height):
        print("\033[38;5;" + borders + "m" + "-" * (5 * width + 1) + "\033[38;5;0m" + " " * (screen_width - 5 * width - 1))
    
        # Here, we assume that each entry of grid is a 4*4 matrix of strings
        strings = [0,0,0,0]
    
        for k in range(4):
            strings[k] = "|" + "|".join(["{:<4}".format("".join(j[k])) for j in grid[i]]) + "|"
            strings[k] += " " * (screen_width - len(strings[k]))

        for k in range(4):
            strings[k] = strings[k].replace(str(turn), "\033[38;5;" + turncolor + "m"+ str(turn) +"\033[38;5;0m")
            strings[k] = strings[k].replace("|", "\033[38;5;" + borders + "m|\033[38;5;0m")
            strings[k] = strings[k].replace("@", "\033[38;5;" + opp + "m@\033[38;5;0m")
            strings[k] = strings[k].replace(myname, "\033[38;5;" + me + "m"+ myname +"\033[38;5;0m")

            for j in specials_list:
                strings[k] = strings[k].replace(j[0], "\033[38;5;"+ j[1] + "m" + j[0]+"\033[38;5;0m")

        for k in range(4):
            print(strings[k])


    print("\033[38;5;"+ borders +"m" + "-" * (5 * width + 1) + "\033[38;5;0m" + " " * (screen_width - 5 * width - 1) + "\033[00m")
    print_log()

def print_log():

    all_background = "208"
    text_color = "46"

    print("\033[48;5;"+ all_background +"m",end="")

    print("\033[38;5;" + text_color + "m" + "-" * 100 + " " * (screen_width - 100) + "\033[38;5;0m")
    print(" " * screen_width)
    print(" " * screen_width)
    print(" " * screen_width)
    
    global log

    for i in log:

        print_string = i[0] + " " * 7 + i[1]
        print_string += " " * (screen_width - len(print_string))
        print("\033[38;5;" + text_color + "m" + print_string + "\033[38;5;0m")
 
    print(" " * screen_width)
    print(" " * screen_width)
    print(" " * screen_width)
    print("\033[38;5;" + text_color + "m" + "-" * 100 + " " * (screen_width - 100) + "\033[38;5;0m")

    print("\033[0m")
    #print("\033[0m", end="")

##### VALIDATION

def get_player(x,y,grid):
    if checkspace(x,y,grid) != "unsafe":
        return "none"
    else:
        if grid[x][y][0][0].lower() == grid[x][y][0][0]:
            return grid[x][y][0][0]
        else:
            if(grid[x][y][0][0] != "S"):
                return grid[x][y][1][0]
            return "none"

def get_turn(x,y,grid):
    if checkspace(x,y,grid) != "unsafe":
        return "none"
    else:
        if grid[x][y][0][0].lower() == grid[x][y][0][0]:
            if(grid[x][y][0][1] == ' '):
                return 0
            return int(grid[x][y][0][1])
        else:
            if (grid[x][y][0][0] != "S"):
                return int(grid[x][y][1][1])
            return "none"

def validate_space(x, y, grid, oldx, oldy):
    if(checkspace(x,oldy, grid) == "unsafe" and checkspace(oldx, y, grid) == "unsafe" and get_player(x,oldy,grid) == get_player(oldx,y,grid) and get_player(oldx, y, grid) != "none" and abs(get_turn(oldx, y, grid) - get_turn(x,oldy, grid)) <= 1):
        return "crossing"
    return checkspace(x, y, grid)

def checkspace(x, y, grid):
    if(grid[x][y][0][0] == " "):
        return "safe"
    if(grid[x][y][0][0] == "S"):
        return "unsafe"
    if(grid[x][y][0][0] != grid[x][y][0][0].lower() and grid[x][y][1][0] == " "):
        return "special"
    return "unsafe"

def checkPossible(x,y,grid):
    for i in range(-1,2):
        for j in range(-1,2):
            if(validate_space((x+i)%size, (y+j)%size, grid, x, y) == "safe"):
                return True
    return False
