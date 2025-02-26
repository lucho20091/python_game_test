import pgzrun
import random

WIDTH = 500
HEIGHT = 400
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

background = Actor('sample')
menu = Actor('sample1')
square = Actor("square")
face = Actor("face")
square.x = 0 + square.width
square.y = 300
face.pos = square.pos
velocity_y = 0
gravity = 1
animation_scheduled = False 
clicked = False
game_over = False
game_started = False  
muted = False

enemies = []
enemies_faces = []
enemies_timeout = 0

button_rect = Rect((WIDTH - BUTTON_WIDTH) // 2, (HEIGHT - BUTTON_HEIGHT) // 2, BUTTON_WIDTH, BUTTON_HEIGHT)


mute_rect = Rect(WIDTH - 100, HEIGHT - 50, 80, 30)


sounds.preview.play(-1)

def update():
    global animation_scheduled, velocity_y, gravity, clicked, enemies_timeout, game_over

    face.pos = square.pos

    if keyboard.up and not clicked:
        clicked = True
        velocity_y = -20
        animation_scheduled = True
        clock.schedule_unique(handle_click, 0.7)
        clock.schedule_unique(animation_still_start, 3.0)
    if keyboard.left:
        animation_scheduled = True
        animation_move()
        clock.schedule_unique(animation_still_start, 3.0)
    if keyboard.down:
        velocity_y = +50
        animation_scheduled = True
        clock.schedule_unique(animation_still_start, 3.0)
    if keyboard.right:
        animation_scheduled = True
        animation_move()
        for actor in enemies:
            actor['actor'].x -= 10
        clock.schedule_unique(animation_still_start, 3.0)
    if not animation_scheduled:
        clock.schedule_unique(animation_still, 5.0) 
        animation_scheduled = True
        # print("Scheduled animation_still")
    square.y += velocity_y
    velocity_y += gravity
    if square.y > 300:
        velocity_y = 0
        square.y = 300
    enemies_timeout += 1
    if enemies_timeout > 100 and game_started:
        actor = Actor('enemie')
        random_number = random.randint(1, 300)
        actor.x = 550
        actor.y = 300
        face_enemie = Actor('face_g')
        face_enemie.pos = actor.pos
        enemies.append({'actor': actor, 'face': face_enemie})
        enemies_faces.append(face_enemie)
        enemies_timeout = 0

    for actor in enemies:
        actor['actor'].x -= 1
        actor['face'].pos = actor['actor'].pos
        if square.colliderect(actor['actor']):
            game_over = True
    
def handle_click():
    global clicked
    clicked = False
def animation_still_start():
    global animation_scheduled
    animation_scheduled = False

def animation_still():
    face.image = "face_j"  
    clock.schedule_unique(animation_still_2, 1.0)

def animation_still_2():
    face.image = "face"  
    global animation_scheduled
    animation_scheduled = False

def animation_move():
    face.image = "face_f"
    global animation_scheduled
    animation_scheduled = False

def end_game():
    global game_started, game_over
    game_started = False
    game_over = False
def draw():
    global game_started
    screen.clear()

    if not game_started:
        menu.draw()
        screen.draw.filled_rect(button_rect, "yellow")
        screen.draw.text("Start Game", center=button_rect.center, fontsize=30, color="black")
    if game_over:
        screen.draw.text("Game Over!", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=40, color="white")
        end_game()
    if not game_over and game_started:
        background.draw()
        square.draw()
        face.draw()
        for actor in enemies:
            actor['actor'].draw()
            actor['face'].draw()

    screen.draw.filled_rect(mute_rect, "red")

    mute_text = "On Music" if muted else "Off Music"
    screen.draw.text(mute_text, center=mute_rect.center, fontsize=20, color="white")


def on_mouse_down(pos):
    global game_started, muted
    
    if button_rect.collidepoint(pos):  
        game_started = True  

    if mute_rect.collidepoint(pos):
        if muted:
            sounds.preview.play(-1)  
        else:
            sounds.preview.stop() 
        muted = not muted  

pgzrun.go()