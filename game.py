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
snake_segments = [[20, 30]]
food_row = food_col = 0
keys = ["d"]
c = 0
previous_positions = [[0, 0]]
apple = "\N{RED APPLE}"
snake = "*"


# update the position  of the new segment added to the snake based on the current direction
def locate_new_segment():
    global snake_segments, c, keys
    # update snake position based on current direction
    if c == "a" or keys[-1] == "a":
        snake_segments[-1][0] = snake_segments[0][0]
        snake_segments[-1][1] = snake_segments[0][1] + 5
    elif c == "s" or keys[-1] == "s":
        snake_segments[-1][0] = snake_segments[0][0] - 5
        snake_segments[-1][1] = snake_segments[0][1]
    elif c == "d" or keys[-1] == "d":
        snake_segments[-1][0] = snake_segments[0][0]
        snake_segments[-1][1] = snake_segments[0][1] - 5
    elif c == "w" or keys[-1] == "w":
        snake_segments[-1][0] = snake_segments[0][0] + 5
        snake_segments[-1][1] = snake_segments[0][1]

        
# function to initialize food location and grow the snake
def init_food_and_extend_snake():
    global snake_segments, food_col, food_row
    if snake_segments[0][1] == food_col and snake_segments[0][0] == food_row:

        #randomly place new food
        food_col = random.randint(3, cols - 3) 
        food_row = random.randint(3, lines - 3)
        
        #add new part to the snake
        snake_segments.append([0, 0])
        locate_new_segment()
   

# move all parts of snake body
def update_snake_body():
    global snake_segments, previous_positions

    # update the body of the snake based on previous previous_positions
    for i in range(len(snake_segments)-1, 0, -1):
        if i > 1:
            snake_segments[i][0] = snake_segments[i-1][0]
            snake_segments[i][1] = snake_segments[i-1][1]

    # move the head of the snake
    if len(snake_segments) >= 2:
        snake_segments[1][0] = previous_positions[-1][0]
        snake_segments[1][1] = previous_positions[-1][1]


# continue moving the snake based on the last pressed key
def continue_move():
    global keys, snake_segments, previous_positions
    
    previous_positions[0][0] = snake_segments[0][0]
    previous_positions[0][1] = snake_segments[0][1]

    if keys[-1] == "a":
        snake_segments[0][1] -= 1
    elif keys[-1] == "s":
        snake_segments[0][0] += 1
    elif keys[-1] == "d":
        snake_segments[0][1] += 1
    elif keys[-1] == "w":
        snake_segments[0][0] -= 1
 
    init_food_and_extend_snake()
    update_snake_body()
    

# move the snake based on the current input    
def move():
    global snake_segments, c, previous_positions
    
    previous_positions[0][0] = snake_segments[0][0]
    previous_positions[0][1] = snake_segments[0][1]
    
    if c == "a":
        snake_segments[0][1] -= 1
    elif c == "s":
        snake_segments[0][0] += 1
    elif c == "d":
        snake_segments[0][1] += 1
    elif c == "w":
        snake_segments[0][0] -= 1

    init_food_and_extend_snake()
    update_snake_body()

    
# initialize game world and food
def init():
    global snake_segments, food_row, food_col

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
    for i in snake_segments:
        stdscr.addch(i[0], i[1], "*")

    #showing food
    stdscr.addch(food_row, food_col, apple)

    #display score
    stdscr.addstr(0, 0, f"{apple} = {len(snake_segments) - 1}", curses.A_STANDOUT)

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
    global snake_segments, playing
    if snake_segments[0][1] == cols:
        playing = False    
    elif snake_segments[0][1] == 0:
        playing = False    
    elif snake_segments[0][0] == lines:
        playing = False    
    elif snake_segments[0][0] == 0:
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
