# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# Define card class
# =================
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# Define hand class
# =================
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        hand_str = ''
        for i in self.hand:
            hand_str = hand_str + str(i)
        return hand_str

    def add_card(self, card):
        self.hand.append(card)

    # ACES
    # ====
    def get_value(self):
        hand_value = 0
        aces = 0
        for i in self.hand:
            if i.get_rank() == 'A':
                aces += 1
            hand_value += VALUES.get(i.get_rank())
        if aces > 0 and (hand_value + 10) <= 21:
            hand_value += 10
        return hand_value

    def draw(self, canvas, pos):
        for i in self.hand:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(i.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(i.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0] + 73 * self.hand.index(i), pos[1] + CARD_CENTER[1]], CARD_SIZE)


# Define deck class
# =================

class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(str(suit), str(rank)))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        self.card = self.deck[0]
        self.deck.remove(self.card)
        return self.card


# Define event handlers for buttons
# =================================
def deal():
    global outcome, score, in_play, my_hand, dealer_hand, deck
    if in_play:
        score -= 1
    my_hand = Hand()
    dealer_hand = Hand()
    deck = Deck()
    deck.shuffle()
    my_hand.add_card(deck.deal_card())
    my_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    outcome = 'Hit or stand?'
    in_play = True

def hit():
    global outcome, score, in_play
    my_hand.add_card(deck.deal_card())
    if my_hand.get_value() > 21:
        outcome = "You busted!"
        score -= 1
        in_play = False
        return score, outcome, in_play
    else:
        outcome = "Hit or stand?"

def stand():
    global outcome, score, in_play
    in_play = False
    if my_hand.get_value() > 21:
        outcome = "You have busted"
        score -= 1
        return score, outcome, in_play
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        else:
            if dealer_hand.get_value() > 21:
                outcome = "Dealer busts, you win. New deal?"
                score += 1
                return score, outcome, in_play
            elif dealer_hand.get_value() >= my_hand.get_value():
                outcome = "Dealer wins. New deal?"
                score -= 1
                return score, outcome, in_play
            else:
                outcome = "You win"
                score += 1
                return score, outcome, in_play

# Draw Handler
# ============

def draw(canvas):
    dealer_hand.draw(canvas, [50, 200])
    my_hand.draw(canvas, [50, 400])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_SIZE)
    canvas.draw_text(outcome,[50,150],30,"White")
    canvas.draw_text("Score: "+str(score),[450,100],25,"White")
    canvas.draw_text("BlackJack",[205,50],45,"White")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
