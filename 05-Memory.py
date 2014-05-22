# Card game - Memory
# ==================

import simplegui
import random

# NEW_GAME. INITIALIZE GLOBAL.
# ============================


def new_game():
    global sum_list_deck, exposed, click_pos_index, state, card1, card2, score
    state = 0
    card1 = False
    card2 = False
    exposed = [False]*16
    list_deck_1 = range(8)
    list_deck_2 = range(8)
    sum_list_deck = list_deck_1 + list_deck_2
    random.shuffle(sum_list_deck)
    score = 0
    label.set_text("Turn = " + str(score))


# Define event handlers
# =====================
def mouseclick(pos):
    # Add game state logic here
    # =========================
    global click_pos_index, exposed, state, card1, card2, score
    click_pos_index = pos[0] // 50

    if exposed[click_pos_index]:
        pass
    elif state == 0:
        global card1
        card1 = (click_pos_index,sum_list_deck[click_pos_index])
        exposed[click_pos_index] = True
        state = 1
        score += 1
        label.set_text("Turn = " + str(score))
    elif state == 1:
        global card2
        card2 = (click_pos_index,sum_list_deck[click_pos_index])
        exposed[click_pos_index] = True
        state = 2

    else:
        if card1[1] != card2[1]:
            exposed[card1[0]] = False
            exposed[card2[0]] = False
            state = 1
            card1 = (click_pos_index,sum_list_deck[click_pos_index])
            exposed[click_pos_index] = True
            score += 1
            label.set_text("Turn = " + str(score))

        else:
            card1 = (click_pos_index,sum_list_deck[click_pos_index])
            exposed[click_pos_index] = True
            state = 1
            score += 1
            label.set_text("Turn = " + str(score))


# DRAW
# ====
def draw(canvas):
    pos = 0
    for index in range(16):
        if exposed[index]:
            canvas.draw_text(str(sum_list_deck[index]), (pos, 85), 100, 'White')
            pos += 50
        else:
            canvas.draw_line([pos+25, 0], [pos+25, 100], 49.5, 'Green')
            pos += 50


# Create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
score = 0
label = frame.add_label("Turns = "+ str(score))

# Register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
