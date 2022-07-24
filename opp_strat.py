def checkPossible(x,y,grid):
    
    for i in range(-1,2):
        for j in range(-1,2):
            if(validate_space((x+i)%size, (y+j)%size, init_grid, x, y) == "safe"):
                return True
    return False

def find_opp_place(x,y,grid):
    pass   
