from tkinter import *
import random
import time

GAME_WIDTH = 1000
GAME_HEIGHT = 700 
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
COLOR_FOOD = "red"
COLOR_SNACK = "green"
BACKGROUND_COLOR = "black"

class Snack:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x , y, x + SPACE_SIZE, y + SPACE_SIZE, fill = COLOR_SNACK, tags = "square")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = COLOR_FOOD, tags = "food")

def next_turn(snack, food):
    global direction, score
    x = snack.coordinates[0][0]
    y = snack.coordinates[0][1]
    
    if direction == "down":
        y += SPACE_SIZE
    elif direction == "up":
        y -= SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snack.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = COLOR_SNACK)
    snack.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        scoreLabel.config(text = f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        if x > canvas.winfo_width():
            snack.coordinates.pop(0)
            canvas.delete(snack.squares[0])
            snack.squares.pop(0)
            snack.coordinates.insert(0, [0, y])
            square = canvas.create_rectangle(0, y, SPACE_SIZE, y + SPACE_SIZE, fill = COLOR_SNACK)
            snack.squares.insert(0, square)
        elif x < 0:
            snack.coordinates.pop(0)
            canvas.delete(snack.squares[0])
            snack.squares.pop(0)
            snack.coordinates.insert(0, [GAME_WIDTH, y])
            square = canvas.create_rectangle(GAME_WIDTH, y, GAME_WIDTH + SPACE_SIZE, y + SPACE_SIZE, fill = COLOR_SNACK)
            snack.squares.insert(0, square)
        elif y > canvas.winfo_height():
            snack.coordinates.pop(0)
            canvas.delete(snack.squares[0])
            snack.squares.pop(0)
            snack.coordinates.insert(0, [x, 0])
            square = canvas.create_rectangle(x, 0,x + SPACE_SIZE, SPACE_SIZE, fill = COLOR_SNACK)
            snack.squares.insert(0, square)
        elif y < 0:
            snack.coordinates.pop(0)
            canvas.delete(snack.squares[0])
            snack.squares.pop(0)
            snack.coordinates.insert(0, [x, GAME_HEIGHT])
            square = canvas.create_rectangle(x, GAME_HEIGHT, x + SPACE_SIZE, GAME_HEIGHT + SPACE_SIZE, fill = COLOR_SNACK)
            snack.squares.insert(0, square)
        snack.coordinates.pop(-1)
        canvas.delete(snack.squares[-1])
        snack.squares.pop(-1)
    if check_colisions(snack) == False:
        window.after(SPEED, next_turn, snack, food)
    else:
        direction = "down"
        game_over()
        
def game_over():
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, text = "GAME OVER", font = ("Arial", 70), fill = "red")
    canvas.create_text(canvas.winfo_width() / 2 , canvas.winfo_height() / 2 + 100, text = "Press Enter to restart", font = ("Arial", 40), fill = "red")

    window.bind("<Return>", lambda event: new_game(event))


def new_game(event):
    window.unbind("<Return>")
    global snack, food, score
    del snack
    del food
    score = 0
    scoreLabel.config(text = f"Score: {score}")
    canvas.delete("all")
    snack = Snack()
    food = Food()
    next_turn(snack, food)

def change_direction(new_direction):
    global direction
    if new_direction == "up":
        if direction != "down":
            direction = "up"
    if new_direction == "down":
        if direction != "up":
            direction = "down"
    if new_direction == "left":
        if direction != "right":
            direction = "left"
    if new_direction == "right":
        if direction != "left":
            direction = "right"

def check_colisions(snack):
    x = snack.coordinates[0][0]
    y = snack.coordinates[0][1]

    for a, b in snack.coordinates[1:]:
        if x == a and y == b:
            return True
    return False
    
window = Tk()
window.title("Snack Game")
window.resizable("False", "False")
score = 0
direction = "down"
scoreLabel = Label(window, text = f"Score: {score}", font = ("Arial", 50))
scoreLabel.pack()
canvas = Canvas(window, bg = BACKGROUND_COLOR, width = GAME_WIDTH, height = GAME_HEIGHT)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

food = Food()
snack = Snack()
next_turn(snack, food)

window.bind("<Left>" , lambda event: change_direction("left"))
window.bind("<Right>" , lambda event : change_direction("right"))
window.bind("<Up>" , lambda event : change_direction("up"))
window.bind("<Down>" , lambda event : change_direction("down"))
window.bind("<A>" , lambda event: change_direction("left"))
window.bind("<D>" , lambda event : change_direction("right"))
window.bind("<W>" , lambda event : change_direction("up"))
window.bind("<S>" , lambda event : change_direction("down"))
window.bind("<a>" , lambda event: change_direction("left"))
window.bind("<d>" , lambda event : change_direction("right"))
window.bind("<w>" , lambda event : change_direction("up"))
window.bind("<s>" , lambda event : change_direction("down"))

window.mainloop()