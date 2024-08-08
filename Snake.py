import random
import tkinter as tk

# Initialising
Grid_size = 25 # 25 by 25 grid
Screen_width = Grid_size*Grid_size
Screen_height = Grid_size*Grid_size
Speed = 100
score = 0
apple = [0,0,False]


# Setting up canvas
window = tk.Tk()
window.title("Snake")

score_text =     'Score        : {}'.format(score)

score_label = tk.Label(window, text= score_text, font=('Arial',15))
score_label.pack(anchor='w')

canvas = tk.Canvas(window, height= Screen_height, width= Screen_width, bg= 'grey')
canvas.pack()

#window.mainloop()

# Snake

snake = [[12,15], [12,16]] # Snake will be an array of coordinates it occupies
direction = 'up'

def move_snake(snake, direction):
    new_head = snake[0].copy()
    
    x = 0 
    y = 1

    #update new head position
    if (direction == 'up'):
        new_head[y] -=1

    elif(direction == 'down'):
        new_head[y] +=1

    elif(direction == 'right'):
         new_head[x] +=1
    
    elif(direction == 'left'):
         new_head[x] -=1

    #create new snake that only has new head
    new_snake = [new_head]

    #append rest of body
    for i in range(1,len(snake)):
        new_snake.append(snake[i-1])

    return new_snake

def draw_snake():
    canvas.delete("snake")  # Remove old snake
    for [x,y] in snake:
        canvas.create_rectangle(
            x * Grid_size,
            y * Grid_size,
            (x + 1) * Grid_size,
            (y + 1) * Grid_size,
            fill="green",
            tag="snake"
        )

def check_collision():
    global snake
    global score
    global apple
    global score_label
    head = snake[0]

    if head == apple[:2] and apple[2]:
        score+=1
        apple[2] = False
        score_label.config(text='Score        : {}'.format(score))
        

    if (head[0] < 0 or head[0] >= Grid_size):
        return True
    
    elif (head[1] < 0 or head[1] >= Grid_size):
        return True
    
    elif (head in snake[1:]):
        return True
    
    return False

def change_direction(event):
    global direction
    new_direction = event.keysym.lower()
    opposite_directions = {
        'up': 'down',
        'down': 'up',
        'left': 'right',
        'right': 'left'
    }
    
    # Prevent the snake from reversing
    if new_direction in opposite_directions and direction != opposite_directions[new_direction]:
        direction = new_direction

window.bind('<Up>', change_direction)
window.bind('<Right>', change_direction)
window.bind('<Down>', change_direction)
window.bind('<Left>', change_direction)

#Apple

def spawn_apple():
    global apple
    x = random.randint(0,24)
    y = random.randint(0,24)
    
    while ([x,y] in snake):
        x = random.randint(0,24)
        y = random.randint(0,24)
    
    apple = [x,y,True]

    return x,y


def draw_apple(x,y):
    canvas.delete("apple")
    canvas.create_rectangle(
            x * Grid_size,
            y * Grid_size,
            (x + 1) * Grid_size,
            (y + 1) * Grid_size,
            fill="red",
            tag="apple"
        )


def Start_Game():
    global snake
    global direction
    tail = snake[-1]
    snake = move_snake(snake, direction)
    if not apple[2]:
        x,y = spawn_apple()
        draw_apple(x,y)
        snake.append(tail)

    
    if (check_collision()):
        return
    
    draw_snake()

    window.after(Speed, Start_Game)  

# Start the game loop
Start_Game()

window.mainloop()