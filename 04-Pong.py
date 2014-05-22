# Implementation of classic arcade game Pong

import simplegui
import random

# Initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
LEFT = False
RIGHT = True
PAD_SPEED = 8  # Add pads speed control, for more customization. =)


# Initialize ball_pos and ball_vel for new bal in middle of table
# If direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == RIGHT:
        ball_vel = [random.randrange(120, 240), random.randrange(60, 180)]
    if direction == LEFT:
        ball_vel = [-random.randrange(120, 240), random.randrange(60, 180)]


# Define event handlers
# =====================
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT/2 - PAD_HEIGHT/2
    paddle2_pos = HEIGHT/2 - PAD_HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    direction = RIGHT  # Add just for first direction of the ball.
    score1 = 0
    score2 = 0
    spawn_ball(direction)


# MOST INTERESTING PART
# =====================
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # ABOUT mid line and gutters
    # ==========================
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")


    # ABOUT BALL
    # ==========
    ball_pos[0] += ball_vel[0] / 60
    ball_pos[1] += ball_vel[1] / 60

    # Collide top
    if ball_pos[1] <= BALL_RADIUS:
        ball_pos[1] = BALL_RADIUS + 1 # Not so dirty trick. Just magic.. Please, don't blame me. =)
        ball_vel[1] = - ball_vel[1]
    # Collide bottom
    elif ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_pos[1] = HEIGHT - BALL_RADIUS - 1 # Not so dirty trick. Just magic.. Please, don't blame me. =)
        ball_vel[1] = - ball_vel[1] # need trick

    # Collide left
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH and paddle1_pos <= ball_pos[1] <= (paddle1_pos + PAD_HEIGHT):
        ball_pos[0]= PAD_WIDTH + 1 + BALL_RADIUS # Not so dirty trick. Just magic.. Please, don't blame me. =)
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] = ball_vel[0] + ball_vel[0] / 10 # boost ball X direction
        ball_vel[1] = ball_vel[1] + ball_vel[1] / 10 # boost ball Y direction
    elif ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        score1 += 1
        return spawn_ball(RIGHT)

    # Collide right
    if ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH and paddle2_pos <= ball_pos[1] <= (paddle2_pos + PAD_HEIGHT):
        ball_pos[0]=WIDTH - 1 - PAD_WIDTH - BALL_RADIUS # Not so dirty trick. Just magic.. Please, don't blame me. =)
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] = ball_vel[0] + ball_vel[0] / 10 # boost ball X direction
        ball_vel[1] = ball_vel[1] + ball_vel[1] / 10 # boost ball Y direction
    elif ball_pos[0] + BALL_RADIUS >= WIDTH:
        score2 += 1
        return spawn_ball(LEFT)


    # ABOUT PADS
    # ==========

    # Update paddle's vertical position.
    if paddle1_vel:
        paddle1_pos += paddle1_vel
    else:
        paddle1_pos -= paddle1_vel

    if paddle2_vel:
        paddle2_pos += paddle2_vel
    else:
        paddle2_pos -= paddle2_vel

    # Keep paddle on the screen!
    # I think, it's nice trick and work fine. =)
    if paddle1_pos < 0:
        paddle1_pos = 0
    elif paddle1_pos > HEIGHT - PAD_HEIGHT:
        paddle1_pos = HEIGHT - PAD_HEIGHT

    if paddle2_pos < 0:
        paddle2_pos = 0
    elif paddle2_pos > HEIGHT - PAD_HEIGHT:
        paddle2_pos = HEIGHT - PAD_HEIGHT


    # DRAW THINGS
    # ===========

    # Draw ball
    canvas.draw_circle((ball_pos[0], ball_pos[1]), BALL_RADIUS, 1, "Red", "White")

    # Draw paddles
    canvas.draw_polygon([[0, paddle1_pos], [PAD_WIDTH, paddle1_pos], [PAD_WIDTH, paddle1_pos + PAD_HEIGHT], [0, paddle1_pos + PAD_HEIGHT]], 1, 'Red', 'Red')
    canvas.draw_polygon([[WIDTH, paddle2_pos], [WIDTH, paddle2_pos+PAD_HEIGHT], [WIDTH-PAD_WIDTH, paddle2_pos + PAD_HEIGHT], [WIDTH-PAD_WIDTH, paddle2_pos]], 1, 'Green', 'Green')

    # Draw scores
    canvas.draw_text(str(score2), (WIDTH/2/2,40), 40, 'Red')
    canvas.draw_text(str(score1), (WIDTH - WIDTH/2/2, 40), 40, 'Green')

    # BONUS Draw PAD_SPEED
    canvas.draw_text("Pad's Speed:", (WIDTH/2/2-80,HEIGHT - 10), 15, 'gray')
    canvas.draw_text(str(PAD_SPEED), (WIDTH/2/2,HEIGHT - 10), 15, 'gray')

    # BONUS BALL_RADIUS
    canvas.draw_text("Ball size:", (WIDTH/2/2-80,HEIGHT - 30), 15, 'gray')
    canvas.draw_text(str(BALL_RADIUS), (WIDTH/2/2 -25,HEIGHT - 30), 15, 'gray')


# DEF HOTKEYS
# ===========
def keydown(key):
    global paddle1_vel, paddle2_vel  #global var
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = - PAD_SPEED
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = PAD_SPEED
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = - PAD_SPEED
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel = PAD_SPEED

def keyup(key):
    global paddle1_vel, paddle2_vel  #global var
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0


# Bonus Features
# ==============
# Size ball
def size_ball_plus():
    global BALL_RADIUS
    if BALL_RADIUS <= 195:
        BALL_RADIUS += 5


def size_ball_minus():
    global BALL_RADIUS
    if BALL_RADIUS >= 10:
        BALL_RADIUS -= 5


def size_ball_norm():
    global BALL_RADIUS
    BALL_RADIUS = 20


# Pad speed
def pad_speed_plus():
    global PAD_SPEED
    if PAD_SPEED < 20:
        PAD_SPEED += 1


def pad_speed_minus():
    global PAD_SPEED
    if PAD_SPEED >= 2:
        PAD_SPEED -= 1


def pad_speed_norm():
    global PAD_SPEED
    PAD_SPEED = 8

# CREATE FRAME
# ============
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_label('Keys:')  # Add Label
frame.add_label('1: up - "w", down-"s"')
frame.add_label('2: up - "up", down-"down"')
frame.add_label(' ')
frame.add_button('+ Ball size', size_ball_plus, 200)
frame.add_button('- Ball size', size_ball_minus, 200)
frame.add_button('Reset ball', size_ball_norm, 200)
frame.add_label(' ')
frame.add_button('+ Pad speed', pad_speed_plus, 200)
frame.add_button('- Pad speed', pad_speed_minus, 200)
frame.add_button('Reset pad', pad_speed_norm, 200)
frame.add_label(' ')
frame.add_label(' ')
frame.add_label(' ')
frame.add_button('RESET GAME', new_game, 200)

# START FRAME
# ===========
new_game()
frame.start()
