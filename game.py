import curses
import random
import time


#initialize the screen and setup color schemes
stdscr = curses.initscr()
curses.start_color()
curses.has_colors()
curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
curses.noecho()
curses.cbreak()
stdscr.keypad(True)


#setup game dimensions and variables
lines = curses.LINES - 1
cols = curses.COLS - 1
world = [] # 2D array representing the game world
players = [[20, 30]]
food_row = food_col = 0
keys = ["d"]
c = 0
moves = [[0, 0]]
apple = "\N{RED APPLE}"
snake = "\N{LARGE BLUE CIRCLE}"


#function to position new part of the snake's body
def locate_new_player():
    global players, c, keys
    # update snake position based on current direction
    if c == "a" or keys[-1] == "a":
        players[-1][0] = players[0][0]
        players[-1][1] = players[0][1] + 5
    elif c == "s" or keys[-1] == "s":
        players[-1][0] = players[0][0] - 5
        players[-1][1] = players[0][1]
    elif c == "d" or keys[-1] == "d":
        players[-1][0] = players[0][0]
        players[-1][1] = players[0][1] - 5
    elif c == "w" or keys[-1] == "w":
        players[-1][0] = players[0][0] + 5
        players[-1][1] = players[0][1]

        
# function to initialize food location and grow the snake
def init_food_player():
    global players, food_col, food_row
    if players[0][1] == food_col and players[0][0] == food_row:

        #randomly place new food
        food_col = random.randint(3, cols - 3) 
        food_row = random.randint(3, lines - 3)
        
        #add new part to the snake
        players.append([0, 0])
        locate_new_player()
   

# move all parts of snake body
def move_all_body():
    global players, moves

    # update the body of the snake based on previous moves
    for i in range(len(players)-1, 0, -1):
        if i > 1:
            players[i][0] = players[i-1][0]
            players[i][1] = players[i-1][1]

    # move the head of the snake
    if len(players) >= 2:
        players[1][0] = moves[-1][0]
        players[1][1] = moves[-1][1]


# continue moving the snake based on the last pressed key
def continue_move():
    global keys, players, moves
    
    moves[0][0] = players[0][0]
    moves[0][1] = players[0][1]

    if keys[-1] == "a":
        players[0][1] -= 1
    elif keys[-1] == "s":
        players[0][0] += 1
    elif keys[-1] == "d":
        players[0][1] += 1
    elif keys[-1] == "w":
        players[0][0] -= 1
 
    init_food_player()
    move_all_body()
    

# move the snake based on the current input    
def move():
    global players, c, moves
    
    moves[0][0] = players[0][0]
    moves[0][1] = players[0][1]
    
    if c == "a":
        players[0][1] -= 1
    elif c == "s":
        players[0][0] += 1
    elif c == "d":
        players[0][1] += 1
    elif c == "w":
        players[0][0] -= 1

    init_food_player()
    move_all_body()

    
# initialize game world and food
def init():
    global players, food_row, food_col

    # create a world
    for l in range(lines):
        world.append([])
        for c in range(cols):
            world[l].append(" ")

    #creating the first food in the game
    food_row = random.randint(3, lines - 3)
    food_col = random.randint(3, cols - 3)
            

# draw the world, snake, and food on the screen
def draw():
    for i in range(lines):
        for j in range(cols):
            stdscr.addch(i, j, world[i][j])   
    #showing snake
    for i in players:
        stdscr.addch(i[0], i[1], "*")

    #showing food
    stdscr.addch(food_row, food_col, apple)

    #display score
    stdscr.addstr(0, 0, f"{apple} = {len(players) - 1}", curses.A_STANDOUT)

    stdscr.refresh()             


# handle user input and update game state
def start():
    global keys, c
    c = stdscr.getkey()
    if c in "asdw":
        move()
        keys[0] = c
    elif c == "q":
        playing = False

    draw()

# end the game if snake hits the walls
playing = True
def finish_game():
    global players, playing
    if players[0][1] == cols:
        playing = False    
    elif players[0][1] == 0:
        playing = False    
    elif players[0][0] == lines:
        playing = False    
    elif players[0][0] == 0:
        playing = False 


#initialize the game
init()
start()
stdscr.nodelay(True)

#main game loop
while playing:
    time.sleep(0.1)
    try:
        c = stdscr.getkey()
    except:
        continue_move()
        c = " "
    if c in "asdw":
        move()
        keys.append(c)
    elif c == "q":
        playing = False
    finish_game()
    draw() 

# end the game and display final message
stdscr.clear()
stdscr.refresh()

stdscr.addstr(int(lines/2), int(cols/2) - 10, "THANKS FOR PLAYING :)",
curses.color_pair(1))
stdscr.refresh()

time.sleep(3)
stdscr.clear()
stdscr.refresh()
curses.endwin()
