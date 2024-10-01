from tkinter import *
import random

#constants
GAME_WIDTH = 700
GAME_HIEGHT = 700
SPEED = 300 #the lower the number the faster the game 90
SPACE_SIZE = 50
BODY_PARTS = 2
SNAKE_COLOR = "#89CFF0"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

#At firt we gave all the objects the atribute pass the we will fill it
#creat class for snake object
class Snake:
    
     def __init__(self):
         
         self.body_size = BODY_PARTS
         self.coordinates = []
         self.ovals = []
         self.eyes = []  # To store references to the eyes
         self.mouth = None  # To store reference to the mouth
        
        #[0,0] to appear in the upper left corner
         for i in range(0, BODY_PARTS):
             self.coordinates.append([0, 0])

             for x, y in self.coordinates:
                 oval = canvas.create_oval(x,y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
                 self.ovals.append(oval)
                 

     def create_eyes(self, x, y, direction):
        # Create eyes for the head of the snake
        eye_radius = SPACE_SIZE // 5
        eye_offset_x = SPACE_SIZE // 2
        eye_offset_y = SPACE_SIZE // 3

        # Calculate eye positions based on the direction of movement
        if direction in ("left", "right"):
            # Horizontal movement (left or right)
            left_eye = canvas.create_oval(x + eye_offset_x, y + eye_offset_y,
                                          x + eye_offset_x + eye_radius, y + eye_offset_y + eye_radius, fill="black")

        else:
            # Vertical movement (up or down)
            left_eye = canvas.create_oval(x + eye_offset_x, y + eye_offset_y,
                                          x + eye_offset_x + eye_radius, y + eye_offset_y + eye_radius, fill="black")


        self.eyes = [left_eye]

     def delete_eyes(self):
        for eye in self.eyes:
            canvas.delete(eye)
        self.eyes = []

     def create_mouth(self, x, y, direction):
        mouth_thickness = 2
        mouth_y_offset = SPACE_SIZE // 1.5
        mouth_x_offset = SPACE_SIZE // 1.5

        if direction == "up":
            self.mouth = canvas.create_line(x + mouth_x_offset, y + mouth_y_offset, 
                                        x + 1.5 * mouth_x_offset, y + 1.5 * mouth_y_offset, fill="black", width=mouth_thickness)  # Diagonal for 'up'
        elif direction == "down":
            self.mouth = canvas.create_line(x + mouth_x_offset, y + mouth_y_offset, 
                                        x + 1.5 * mouth_x_offset, y + 1 * mouth_y_offset, fill="black", width=mouth_thickness)  # Diagonal for 'down'
        elif direction == "left":
            self.mouth = canvas.create_line(x + mouth_y_offset, y + mouth_x_offset, 
                                        x + 1.3 * mouth_y_offset, y + 1 * mouth_x_offset, fill="black", width=mouth_thickness)  # Diagonal for 'left'
        elif direction == "right":
            self.mouth = canvas.create_line(x + mouth_y_offset, y + mouth_x_offset, 
                                       x + 1.7 * mouth_y_offset, y + 1.5 * mouth_x_offset, fill="black", width=mouth_thickness)  # Diagonal for 'right'
     
     def delete_mouth(self):
        if self.mouth:
            canvas.delete(self.mouth)
            self.mouth = None

#creat class for food object
class Food:

    #constroct food object
    def __init__(self):
    
    #second number = GAME_WIDTH or GAME_HIEGHT/ SPACE_SIZE so 700/50 = 14
    #* by SPACE_SIZE to turn it into a pixel
        x = random.randint(0,int((GAME_WIDTH/SPACE_SIZE)-1)) * SPACE_SIZE
        y = random.randint(0,int((GAME_HIEGHT/SPACE_SIZE)-1)) * SPACE_SIZE

        self.coordinates = [x,y]

        #X and y plus the size of any object in the game
        canvas.create_oval(x,y, x + SPACE_SIZE/1.3, y + SPACE_SIZE/1.3, fill=FOOD_COLOR, tag="food") 

#the functions that we're gonna use with pass as well
def next_turn(snake, food):
    
    x,y = snake.coordinates[0] #coordinates for head of the snake

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    elif direction == "left":       
        x -= SPACE_SIZE

    snake.coordinates.insert(0, [x, y])

    oval = canvas.create_oval(x, y, x +SPACE_SIZE, y+ SPACE_SIZE, fill=SNAKE_COLOR)
    
    # Delete the old eyes and mouth before creating new ones
    snake.delete_eyes()
    snake.delete_mouth()

    # Create eyes and mouth for the new head position
    snake.create_eyes(x, y, direction)
    snake.create_mouth(x, y, direction)
    
    snake.ovals.insert(0, oval)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        
        global score

        score += 1

        Label.config(text="score:{}".format(score))

        canvas.delete("food")

        food = Food()
    else:
        del snake.coordinates[-1]

        canvas.delete(snake.ovals[-1])

        del snake.ovals[-1]
    
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
            
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'updd':
            direction = new_direction        

def check_collisions(snake):
    
    x,y = snake.coordinates[0]

#    if x < 0 or x >= GAME_WIDTH:
#        return True
#    elif y < 0 or y >= GAME_HIEGHT:
#        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
        
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas',70), text="GAME OVER", fill="red",tag="gameover")

window = Tk()
window.title("Snakie")
window.resizable(False, False) #to not let the window change size

score = 0
direction = 'down'

Label= Label(window, text="score:{}".format(score), font=('consola', 40)) #consola is a font name and 40 is for size
Label.pack()

canvas = Canvas(window ,bg=BACKGROUND_COLOR, height=GAME_HIEGHT, width=GAME_WIDTH)
canvas.pack()

#to make the screen appear in the middle
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

#take the screen and devide it by 2 to get the center for width and height for screen aka monitor and the game window (very smart very demior)
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<w>',lambda event: change_direction('up'))
window.bind('<a>',lambda event: change_direction('left'))
window.bind('<s>',lambda event: change_direction('down'))
window.bind('<d>',lambda event: change_direction('right'))

window.bind('<W>',lambda event: change_direction('up'))
window.bind('<A>',lambda event: change_direction('left'))
window.bind('<S>',lambda event: change_direction('down'))
window.bind('<D>',lambda event: change_direction('right'))  

window.bind('<Up>' ,lambda event: change_direction('up'))
window.bind('<Left>' ,lambda event: change_direction('left'))
window.bind('<Down>' ,lambda event: change_direction('down'))
window.bind('<Right>' ,lambda event: change_direction('right'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()