
import pygame as pg;
import ast;
import time;
import heapq;
from random import random;
import math;


no = 0
MAZE_PATH = "./Data/data" + str(no) + ".txt"
ROBOTS_PATH = "./Data/Robots" + str(no) + ".txt"
AGENTS_PATH = "./Data/Agent" + str(no) + ".txt"

MAP = []
AGENTS = []
AGENTS_POSITION = []
ROBOTS = []
WIDTH = 1000
HEIGHT = 600

class Cell:
    def __init__(self):
      # Parent cell's row index
        self.parent_i = 0
    # Parent cell's column index
        self.parent_j = 0
 # Total cost of the cell (g + h)
        self.f = float('inf')
    # Cost from start to this cell
        self.g = float('inf')
    # Heuristic cost from this cell to destination
        self.h = 0
    
    #TO MANAGE THE PATH WHEN THE CELL IS BLOCKED BY AGENT 
        self.repeat = False


# READING THE MAP
def maze_reading():
   
    try:    
        with open(MAZE_PATH , 'r') as text_file:
            lines = int(text_file.readline())
            for line in text_file:
                line = list(line[:-1])
                MAP.append(line)
    except:
        print("Error in reading Maze File")
    return lines

def parsing_robots():
    """
    ROBOTS STRUCTURE 
    robots = [ 
        { 
            start : (x,y),
            end : (x,y),
        }
    ]
    """    
    # end def
    try:
        with open(ROBOTS_PATH , 'r') as text_file:
            for line in text_file:
                # SPLITING THE LINE TO GET THE COORDINATES
                line1 = line.split(":")[1].split(" ")
                startx = line1[2][1:-1]
                starty = line1[3][0:-1]
                endx = line1[5][1:-1]
                endy = line1[6][0:-2]
                ROBOTS.append({
                    "start" : [int(startx) , int(starty)],
                    "end" : [int(endx) , int(endy)]
                })
                
                
    except Exception as e:
        print("Error in reading robots File" ,e)

def parsing_agents():
    """
    AGENTS STRUCTURE 
    AGENTS = [ 
        { 
            postion : [(x,y),(x,y),(x,y)],
            time : [1,2,3,],
        }
    ]
    
    """
    try:
        with open(AGENTS_PATH , 'r') as text_file:
            for line in text_file:
                line  = line[:-1]
                line1 = line.split(":")[1].split(" at times ")
                line1[0] = f'[{line1[0][3:-2]}]'
                agents_postion = ast.literal_eval(line1[0])  # abstract syntax tree used here to convert string to tuple
                time = ast.literal_eval(line1[1])   

                #REARRANGING THE LIST agent_position WITH RESPECT TO THE TIME
                temp = [None]* len(agents_postion)

                for i in range(len(temp)):
                    temp[time[i]] = agents_postion[i]
                AGENTS.append({
                    "position" : temp,
                    "time" : time
                })
                # UPDATING THE ARRAY WITH CURRENT POSITION
                AGENTS_POSITION.append(AGENTS[-1]["position"][0])   
                
    except Exception as e:
        print("Error in reading agents File",e)

def draw_styled_rect(screen, color, position, border_color=(0, 0, 0), border_thickness=2, rounded_corners=True):
    try:
        # Draw the rectangle with optional rounded corners
        if rounded_corners:
            pg.draw.rect(screen, color, position, border_radius=10)  # Rounded corners
        else:
            pg.draw.rect(screen, color, position)
        # Add the border
        pg.draw.rect(screen, border_color, position, border_thickness, border_radius=10 if rounded_corners else 0)

    except Exception as e:
        print(f"Error: {e}")

def update_screen(screen,changed ,cell_width, cell_height):
   
    if changed:
        # DRAWING THE OUTER BOUNDARY
        boundary_thickness = 10
        pg.draw.rect(screen, (0, 0, 0), (10, 10, WIDTH - 20, HEIGHT - 20), boundary_thickness)
        
        # DRAWING THE MAZE AND SPACE AND OBSTACLE
        for i in range(len(MAP)):
            for j in range(len(MAP[i])):
                if MAP[i][j] == 'X':  # Wall
                    draw_styled_rect(screen, (80, 80, 200), position=(20 + j * cell_width, 20 + i * cell_height, cell_width, cell_height))          
                else: 
                    draw_styled_rect(screen, (255, 255, 255), position=(20 + j * cell_width, 20 + i * cell_height, cell_width, cell_height))  

        # DRAWING THE ROBOT RED CIRCLES
        for i in range(len(ROBOTS)):
            pg.draw.circle(
                screen, 
                (255, (i * 20) % 256, (i * 40) % 256), 
                (20 + ROBOTS[i]["start"][1] * cell_width + cell_width // 2, 
                20 + ROBOTS[i]["start"][0] * cell_height + cell_height // 2), 
                cell_width // 3
            )
        # DRAWING THE AGENT YELLOW CIRCLES
        for agent in AGENTS_POSITION:
            pg.draw.circle(screen, (255, 255, 0), (20 + agent[1] * cell_width + cell_width // 2, 20 + agent[0] * cell_height + cell_height // 2), cell_width // 3)
        changed = False

    pg.display.update()

def update_agents():
    for agent in AGENTS:
        agent["position"] = agent["position"][agent["time"].index(min(agent["time"]))]

def cal_distance(start, end):
    # return abs(start[0] - end[0]) + abs(start[1] - end[1])
    return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5

def is_blocked(row, col):
    # THE (ROW,COL) HAVE IS HAVE THE OBSTACLE OR NOT 
    inbound = row < 0 or row >= len(MAP) or col < 0 or col >= len(MAP[0])
    return inbound or MAP[row][col] == 'X'

def is_have_agent(row ,col):
    # THE (ROW,COL) HAVE IS ACCUPIED BY AGENT OR NOT 
    for agent in AGENTS:
        if(agent == (row, col)):
            return True
    
def is_have_robot(row, col):
    # THE (ROW,COL) HAVE IS ACCUPIED BY ROBOT OR NOT 
    for robot in ROBOTS:
        if(robot == [row, col]):
            return True  


def move_agent():   
    for agent in AGENTS:
        pass

def random_move_robot(current , i , j):
    
    """
        0 -> same 
        1-> left
        2-> right
        3 -> up
        4 -> down
    """
    while True:            
        direction1 = math.floor(random() * 5)
        print("The random move for first", direction1)
        if(direction1 == 0): break
        if direction1 == 1 and current[1]-1 >= 0 and MAP[current[0]][current[1]-1] != 'X':
            ROBOTS[i]["start"] = [current[0] , current[1] -1]
            break
        elif direction1 == 2 and current[1]+1 < len(MAP) and MAP[current[0]][current[1]+1] != 'X':
            ROBOTS[i]["start"] = [current[0] , current[1]+1]
            break
        elif direction1 == 3 and current[0] >= 0 and MAP[current[0]-1][current[0]] != 'X':
            ROBOTS[i]["start"] = [current[0]-1 , current[1]]
            break
        elif direction1 == 4 and current[0] < len(MAP[0]) and MAP[current[0]+1][current[0]] != 'X':
            ROBOTS[i]["start"] = [current[0]+1, current[1]]
            break

    while True:            
        print("The random move for first", direction1)
        direction1 = math.floor(random() * 5)
        if(direction1 == 0): break
        if direction1 == 1 and current[1]-1 >= 0 and MAP[current[0]][current[1]-1] != 'X':
            ROBOTS[j]["start"] = [current[0] , current[1] -1]
            break
        elif direction1 == 2 and current[1]+1 < len(MAP) and MAP[current[0]][current[1]+1] != 'X':
            ROBOTS[j]["start"] = [current[0] , current[1]+1]
            break
        elif direction1 == 3 and current[0] >= 0 and MAP[current[0]-1][current[0]] != 'X':
            ROBOTS[j]["start"] = [current[0]-1 , current[1]]
            break
        elif direction1 == 4 and current[0] < len(MAP[0]) and MAP[current[0]+1][current[0]] != 'X':
            ROBOTS[j]["start"] = [current[0]+1, current[1]]
            break

        


# CHECK THE COLLISION BETWEEN AMONG ROBOTS
def check_collision_among_robots(path,itr,itr_agents,agents_direction):
     for i in range(len(ROBOTS)):
        for j in range(i+1,len(ROBOTS)):
            if(ROBOTS[i]["start"] == ROBOTS[j]["start"]):
                print("COLLISION DETECTED WITH AMONG ROBOTS AT",ROBOTS[j]["start"])
                #IF COLLISION DETECTED MOVE THE ROBOTS ONE STEP BACK
                # ROBOTS[i]["start"] = path[i][itr[i]-2]
                # ROBOTS[j]["start"] = path[j][itr[j]-2]
                random_move_robot(ROBOTS[i]["start"] , i , j)
                print(ROBOTS[i]["start"])
                print(ROBOTS[j]["start"])
                #CALCULATED NEW PATH
                path[i] = A_star_individual(ROBOTS[i],i,False,itr_agents,agents_direction)
                path[j] = A_star_individual(ROBOTS[j],j,False,itr_agents,agents_direction)
                
                itr[i] = 0
                itr[j] = 0
                return True

def check_collision_with_agents(path , itr , itr_agents,agents_direction):

    # CHECK THE COLLISION BETWEEN EACH ROBOT AND EACH AGENT
    for i in range(len(ROBOTS)):
        for agent in AGENTS_POSITION:
            if(ROBOTS[i]["start"] == agent):
                print("COLLISION DETECTED WITH AGENTS")
                # ROBOTS[i]["start"] = path[i][itr[i]-2]
                path[i] = A_star_individual(ROBOTS[i],i)
                itr[i] = 0
                return True


def trace_path(cell_details, dest ,isfirst):
    print("TRACING THE PATH ")
    path = []
    row = dest[0]
    col = dest[1]
    loop = 0
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        if cell_details[row][col].repeat:
            print("Repeated->" ,(row,col))
            path.append((row, col))
            path.append((temp_row, temp_col))
        path.append((row, col))
        row = temp_row
        col = temp_col
        loop +=1

    # Add the source cell to the path
    path.append((row, col))
    # Reverse the path to get the path from source to destination
    path.reverse()
    print("PATH TRACED SUCCESSFULLY ")
    return path


def calculate_agents_position(row,col,time_passed,agents_itr=None,agents_direction=None):

    
    i = 0
    for agent in AGENTS:
        if agents_direction:
            print(agents_direction,agents_itr,time_passed)
        left = time_passed % len(agent["position"])
        itration_done = time_passed // len(agent["position"])
        current_index = 0

        #IF ITS FIRST TIME TO RUN THE A_STAR
        if agents_itr == None or agents_itr[i] == 0:
            if itration_done != 0 and itration_done % 2 == 0:
                 current_index = len(agent["position"]) - left - 1 
            else:
                current_index =  left  

        #IF A_STAR IS RUNNING BECAUSE OF THE COLLISION
        else:
            #CHECK IN WHIHC DIRECTION THE AGENT IS MOVING
            if agents_direction[i]:
                #IF AGENT IS MOVING (LEFT TO RIGHT) ACCORDING TO INDICES THEN NEXT TIME IT MOVE RIGHT TO LEFT
                current_index  = (agents_itr[i] + left) %  len(agent["position"])
                if current_index > 0:
                  current_index = len(agent["position"]) - (left - 1)
                else:
                    current_index = agents_itr[i] + left
            # IF DIRECTION IS RIGHT TO LEFT
            else:
                if (agents_itr[i] - left < 0):
                    current_index = -(left - 1)
                else :
                    current_index = agents_itr[i] - left 
        if agent["position"][current_index] == (row, col):
            print("EXPECTED COLLISION BETWEEN AGENT AND ROBOT" , (row, col),itration_done,left)
            return True
        i+=1
    return False

def explore_the_path(dir,goal,current,cell_detail,closed_list,isfirst,itr_agents,agents_direction,open_list):
     
        is_blocked_by_agent = False

        new_row = current[0] + dir[0] 
        new_col = current[1] + dir[1] 

        # CHECK IF THE NEW BLOCK IS VALID FOR MOVEMENT
        is_obstacle = is_blocked(new_row , new_col)
        in_closed_list  = str([new_row , new_col]) in closed_list

        #CHECK IF THE AGENT WILL BE AT THE CURRENT CELL IN FUTURE
        if not isfirst:
            is_agent_collision =  calculate_agents_position(new_row, new_col,int(cell_detail[current[0]][current[1]].g),itr_agents,agents_direction)
        else:
            is_agent_collision =  calculate_agents_position(new_row, new_col,int(cell_detail[current[0]][current[1]].g))
        if not is_obstacle and not in_closed_list and is_agent_collision:
            is_blocked_by_agent = True
        
        if not is_obstacle and not is_agent_collision and not in_closed_list:
            is_blocked_by_agent = False

            # CLACULATE THE NEXT f,g,h
            g_new = cell_detail[current[0]][current[1]].g + 1.0
            h_new = cal_distance((new_row, new_col), goal)
            f_new = g_new + h_new

            #UPDATE THE CELL DETAILS
            if cell_detail[new_row][new_col].f == float('inf') or cell_detail[new_row][new_col].f > f_new:
                cell_detail[new_row][new_col].parent_i = current[0]
                cell_detail[new_row][new_col].parent_j = current[1]
                cell_detail[new_row][new_col].f = f_new
                cell_detail[new_row][new_col].g = g_new
                cell_detail[new_row][new_col].h = h_new
                heapq.heappush(open_list,(f_new,[new_row,new_col]))
        if(is_blocked_by_agent):
            cell_detail[current[0]][current[1]].g += 10 
            cell_detail[current[0]][current[1]].f += 10 
            heapq.heappush(open_list,(int(cell_detail[current[0]][current[1]].f),[current[0],current[1]]))
            cell_detail[current[0]][current[1]].repeat = True 
        

def A_star_individual(robot , i ,isfirst = False,itr_agents=None,agents_direction=None):

    closed_list = set()
    open_list = []
    goal = robot["end"]
    start = robot["start"]
    direction = [(1,0),(-1,0),(0,-1),(0,1)]
    heapq.heappush(open_list,(0,start))

    cell_detail = [[Cell() for _ in range(len(MAP[0]))] for _ in range(len(MAP))]

    cell_detail[start[0]][start[1]].f = 0 
    cell_detail[start[0]][start[1]].g = 0 
    cell_detail[start[0]][start[1]].h = 0 
    cell_detail[start[0]][start[1]].parent_i = start[0] 
    cell_detail[start[0]][start[1]].parent_j = start[1]

    loop = 0
    while len(open_list) > 0:   #until queue is not empty
        current = heapq.heappop(open_list)[1]
        closed_list.add(str(list(current)))
        if(current == goal): 
            print("PATH COMPLETED FOR THE ROBOT",i)
            path =  trace_path(cell_detail,goal,isfirst)
            print(path)
            return path
        
        #LOOKING FOR BEST MOVE
        for dir in direction: 
           explore_the_path(dir,goal,current,cell_detail,closed_list,isfirst,itr_agents,agents_direction,open_list)
        loop+=1

    print(f"No path for robot {i}")
    return []

def A_star():
    path = []
    for i in range(len(ROBOTS)):
       print(f"A STAR CALLED FOR ROBOT {i}")
       path.append(A_star_individual(ROBOTS[i],i,True))
       print(f"A STAR COMPLETED FOR ROBOT {i}")
    return path


def main():
    

    # INTIALIZING THE MAZE
    print("PARSING STARTED")
    lines = maze_reading()
    parsing_robots()
    parsing_agents()
    print("PARSING COMPLETED SUCCESSFULLY")
    
    
    Running = True
    changed = True
    print("A STAR STARTED")
    path = A_star()
    print("PATH CALCULATED SUCCESSFULLY")

    # INTIALIZING PYGAME
    pg.init()
    pg.display.set_caption("Maze Game")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill((255, 255, 255)) 

    cell_height = (HEIGHT - 40) / lines
    cell_width = (WIDTH - 40) / len(MAP[0])

    if(cell_height < 1): cell_height = 1
    if(cell_width < 1): cell_width = 1


    #TWO ARRAY TO DECIDE THE NEXT POSITION FOR AGENT AND ROBOT
    # THEY STORE THE INDEX FOR CURRENT POSISTION FOR ROBOTS AND AGENTS
    itr = [1 for _ in range(len(ROBOTS))]  
    itr_agents = [0 for _ in range(len(AGENTS))]
    agents_direction = [True for _ in range(len(AGENTS))]
    time_taken = [1 for _ in range(len(ROBOTS))]

    for i in range(len(path)):
        print("PATH FOR ROBOT" ,i, path[i])
    for i in range(len(path)):
        print(f"INTIAL TIME ESTIMATION FOR ROBOT_{i} {len(path[i])}")
    
    print(len(MAP),len(MAP[0]))

    count = 0
    #MAIN GAME LOOP
    while Running:
        update_screen(screen,changed,cell_width, cell_height)
        #LOOKING FOR THE WINDOW EVENTS
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Running = False
                break

        # MOVING THE ROBOTS
        for i in range(len(ROBOTS)):
            if itr[i] < len(path[i]):
                ROBOTS[i]["start"] = path[i][itr[i]]
                itr[i] += 1
                time_taken[i] +=1
                if(itr[i] == len(path[i])):
                    print(F"TIME TAKEN BY ROBOT {i} {time_taken[i]}")
                    print(F"ROBOT {i} HAVE SUCCESSFULLY REACHED TO DESTINATION")
                    # count +=1
        
        # MOVING THE AGENTS
        for i in range(len(AGENTS)):
            AGENTS_POSITION[i] = AGENTS[i]["position"][itr_agents[i]]
            if agents_direction[i]:
                itr_agents[i] += 1
            else:
                itr_agents[i] -= 1

            if itr_agents[i] >= len(AGENTS[i]["position"]):
                itr_agents[i] = len(AGENTS[i]["position"]) - 1
                agents_direction[i] = False
            elif itr_agents[i] < 0:
                itr_agents[i] = 0
                agents_direction[i] = True
            
            itr_agents[i] = (itr_agents[i] + 1) % len(AGENTS[i]["position"]) 

       # check_collision_with_agents(path ,itr,itr_agents,agents_direction)
        check_collision_among_robots(path ,itr,itr_agents,agents_direction)
        time.sleep(1)

        if(count == len(ROBOTS)):   
            print("ALL ROBOTS SUCCESSFULLY REACHED TO DESTINATION")
            break
    pg.quit()

if __name__ == "__main__":
    main()

