#https://www.youtube.com/watch?v=bfRwxS5d0SI&t=1099s
from tkinter import *
import random
from PIL import Image, ImageTk  # Import the necessary modules from PIL

#constants
GAME_WIDTH = 700
GAME_HIEGHT = 700
SPEED = 200 #the lower the number the faster the game 90
SPACE_SIZE = 60
BODY_PARTS = 2
SNAKE_COLOR = "#89CFF0"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

window = Tk()
window.title("Snake and Gigachad")
window.resizable(False, False) #to not let the window change size

# Load and resize the image globally to ensure it's available
gigacgad_original_image = Image.open("C:\\Users\\KSA\\Documents\\GitHub\\Snake\\Snakie\\Images\\Giga-chad-transparent.png")
image_size = (90, 90)  # Define consistent size
resized_image = gigacgad_original_image.resize(image_size, Image.LANCZOS)
global_image = ImageTk.PhotoImage(resized_image)

# Create both the right-facing and left-facing versions
global_image_right = ImageTk.PhotoImage(resized_image)
global_image_left = ImageTk.PhotoImage(resized_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT))

# rotated_image = resized_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

right_legs_original_image = Image.open("C:\\Users\\KSA\\Documents\\GitHub\\Snake\\Snakie\\Images\\Right-Legs.png")

# Assume each frame is the same size
FRAME_WIDTH = 130  # Set this to your frame's width
FRAME_HEIGHT = 180  # Set this to your frame's height

num_of_frames = 6

# Resize the frames to 10x10 as desired
RESIZED_WIDTH = 100  # Your desired width
RESIZED_HEIGHT = 100  # Your desired height

frames = []

for i in range(num_of_frames):
    # Define the box to extract the frame (left, upper, right, lower)
    box = (i * FRAME_WIDTH, 0, (i + 1) * FRAME_WIDTH, FRAME_HEIGHT)
    frame = right_legs_original_image.crop(box)

    # Resize the extracted frame
    resized_frame = frame.resize((RESIZED_WIDTH, RESIZED_HEIGHT), Image.LANCZOS)

    frames.append(resized_frame)

# Convert frames to tkinter-compatible images
tk_frames = [ImageTk.PhotoImage(frame) for frame in frames]

left_legs_original_image = Image.open("C:\\Users\\KSA\\Documents\\GitHub\\Snake\\Snakie\\Images\\Left-Legs.png")

frames_L = []

for i in range(num_of_frames):
    # Define the box to extract the frame (left, upper, right, lower)
    boxL = (i * FRAME_WIDTH, 0, (i + 1) * FRAME_WIDTH, FRAME_HEIGHT)
    frame_L = left_legs_original_image.crop(boxL)

    # Resize the extracted frame
    resized_frame_L = frame_L.resize((RESIZED_WIDTH, RESIZED_HEIGHT), Image.LANCZOS)

    frames_L.append(resized_frame_L)

# Convert frames to tkinter-compatible images
tk_frames_L = [ImageTk.PhotoImage(frame_L) for frame_L in frames_L]




canvas = Canvas(window ,bg=BACKGROUND_COLOR, height=GAME_HIEGHT, width=GAME_WIDTH)
canvas.pack()

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
    
        self.is_facing_left = True  # Initialize facing right
        self.image = global_image_right  # Use the right-facing image initially

        # Determine initial direction based on snake's position
        snake_x, _ = snake.coordinates[0]
        # second number = GAME_WIDTH or GAME_HIEGHT/ SPACE_SIZE so 700/50 = 14
        # * by SPACE_SIZE to turn it into a pixel
        x = random.randint(0, int((GAME_WIDTH/SPACE_SIZE)-1)) * SPACE_SIZE
        y = random.randint(0, int((GAME_HIEGHT/SPACE_SIZE)-1)) * SPACE_SIZE

        if x < snake_x:
            self.is_facing_left = True
            self.image = global_image_left
        else:
            self.image = global_image_right

        self.coordinates = [x,y]

        #X and y plus the size of any object in the game
        self.food_oval = canvas.create_oval(x,y, x + SPACE_SIZE/1.6, y + SPACE_SIZE/1.6, fill=FOOD_COLOR, tag="food") 
        # Adjust the (x, y) coordinates to center it on the oval
        self.food_image = canvas.create_image(x + SPACE_SIZE / 3, y + SPACE_SIZE / 2.6, image=self.image, tag="gigachad")

    def move_away_from_snake(self, snake):
        # Get current position
        x, y = self.coordinates
        snake_x, snake_y = snake.coordinates[0]

        # Determine if the food should move left or right
        if snake_x > x:  # Snake is to the right of food, move food left
            x -= 5
            # Flip image to face left if needed
            if not self.is_facing_left:
                self.is_facing_left = True
                self.update_image(flip=False)
                animated_food.update_position(x, y, is_facing_left=True) # Update direction for animation
        elif snake_x < x:  # Snake is to the left of food, move food right
            x += 5
            # Flip image to face right if needed
            if self.is_facing_left:
                self.is_facing_left = False
                self.update_image(flip=True)
                animated_food.update_position(x, y, is_facing_left=False) # Update direction for animation
            
        # Check for boundaries to keep food inside the game area
        if x <= 0:
            x += 5
        elif x >= (GAME_WIDTH - SPACE_SIZE):
            x = GAME_WIDTH - SPACE_SIZE

        if y <= 0:
            y += 5
        if snake_y > y:
            y -= 5  # Move up
        if y >= (GAME_HIEGHT - SPACE_SIZE):
            y -= 5
        elif snake_y < y:
            y += 5  # Move down

        # Update position
        self.coordinates = [x, y]

        # Move the food's canvas items to the new position
        canvas.coords(self.food_oval, x, y, x + SPACE_SIZE / 1.6, y + SPACE_SIZE / 1.6)
        canvas.coords(self.food_image, x + SPACE_SIZE / 3, y + SPACE_SIZE / 2.6)

        # Update the animation's position to follow the food
        animated_food.update_position(x, y)

    # Function to flip the image based on the direction
    def update_image(self, flip):

        if flip:
            # Use the preloaded left-facing image
            self.image = global_image_left
        else:
            # Use the preloaded right-facing image
            self.image = global_image_right

        # Update the image on the canvas
        canvas.itemconfig(self.food_image, image=self.image)

class AnimatedFood:
    def __init__(self, canvas, right_frames, left_frames, x, y):
        self.canvas = canvas
        self.right_frames = right_frames
        self.left_frames = left_frames
        self.current_frames = right_frames
        self.frame_index = 0
        self.image_id = None
        self.is_animating = True
        self.is_facing_left = False # Keep track of current direction

        # Initial position of the animation (can be updated later)
        self.x = x
        self.y = y 

        # Display the first frame (position will be updated to follow food)
        self.image_id = self.canvas.create_image(self.x, self.y, image=self.current_frames[self.frame_index], anchor='nw')

        # Start animation
        self.animate()

    def animate(self):
        if self.is_animating:
            # Update the frame
            self.frame_index = (self.frame_index + 1) % len(self.current_frames) # Loop through frames
            self.canvas.itemconfig(self.image_id, image=self.current_frames[self.frame_index])

            # Schedule the next frame update
            self.canvas.after(100, self.animate) # Adjust 100 for speed (milliseconds)

    def update_position(self, x, y, is_facing_left = None):
        # Update the animation's position to follow the food's new coordinates
        if is_facing_left == False:
            self.x = x - 25
            self.y = y + 15
            self.canvas.coords(self.image_id, self.x, self.y)
        else:
            self.x = x - 40
            self.y = y + 15
            self.canvas.coords(self.image_id, self.x, self.y)

        # Update direction if specified
        if is_facing_left is not None and is_facing_left != self.is_facing_left:
            self.is_facing_left = is_facing_left
            #switch frames based on direction
            self.current_frames = self.left_frames if is_facing_left else self.right_frames
            self.frame_index = 0

def is_snake_nearby(snake, food):
    # Snake's head coordinates
    snake_x, snake_y = snake.coordinates[0]

    # Food coordinates
    food_x, food_y = food.coordinates
    food_center_x = food_x + SPACE_SIZE / 2
    food_center_y = food_y + SPACE_SIZE / 2

    # Determine the range for both x and y
    snake_x_range = (snake_x, snake_x + SPACE_SIZE)
    snake_y_range = (snake_y, snake_y + SPACE_SIZE)

    # Check if the food's center falls within the snake's proximity range
    is_within_x = (snake_x <= food_center_x < snake_x + SPACE_SIZE)
    is_within_y = (snake_y <= food_center_y < snake_y + SPACE_SIZE)

    # Check if both x and y are within the defined proximity range
    return is_within_x and is_within_y

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

    # Handle screen wrapping
    if x >= GAME_WIDTH:
        x = 0
    elif x < 0:
        x = GAME_WIDTH - (GAME_WIDTH % SPACE_SIZE)
    elif y >= GAME_HIEGHT:
        y = 0
    elif y < 0:
        y = GAME_HIEGHT - (GAME_HIEGHT % SPACE_SIZE)

    snake.coordinates.insert(0, [x, y])

    oval = canvas.create_oval(x, y, x +SPACE_SIZE, y+ SPACE_SIZE, fill=SNAKE_COLOR)
    
    # Delete the old eyes and mouth before creating new ones
    snake.delete_eyes()
    snake.delete_mouth()

    # Create eyes and mouth for the new head position
    snake.create_eyes(x, y, direction)
    snake.create_mouth(x, y, direction)
    
    snake.ovals.insert(0, oval)

    # if x == food.coordinates[0] and y == food.coordinates[1]:

    # Check if the snake is close enough to eat the food
    if is_snake_nearby(snake, food):
        global score

        score += 1

        Label.config(text="score:{}".format(score))

        canvas.delete("food")
        canvas.delete("gigachad")

        food = Food()
    else:
        del snake.coordinates[-1]

        canvas.delete(snake.ovals[-1])

        del snake.ovals[-1]

    # Move food towards the snake
    food.move_away_from_snake(snake)
    
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
        if direction != 'up':
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

# Assuming you have already loaded the animation frames
animation_frames = [ImageTk.PhotoImage(frame) for frame in frames]  # Replace 'frame_list' with your actual frames

# Create an instance of AnimatedFood outside the Food class
animated_food = AnimatedFood(canvas, tk_frames, tk_frames_L, 0, 0)

score = 0
direction = 'down'

Label= Label(window, text="score:{}".format(score), font=('consola', 40)) #consola is a font name and 40 is for size
Label.pack()

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