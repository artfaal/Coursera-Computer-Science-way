import simplegui
import math
import random


# Initialize global variables used in your code
# ==============================================


num_range = 100
secret = 0
count = 0
guess = 0


# Helper function to start and restart the game
# =============================================


def new_game():
    global secret
    # Generate secret number
    secret = int(random.randrange(0, num_range))

    # Show range
    print "\nNew game. Range is from 0 to %d" % num_range

    # Generate/Update number of tries (count). Challenge accepted! =)
    int(num_of_try(num_range))

    # Print new count of tries.
    print "Number of remaining guess is %d" % count

    # In this step you input information on input line
    # and go to main def
    return input_guess(f.add_input)


# Define event handlers for control panel
# =======================================


def range100():
    # Update global range
    global num_range
    num_range = 100
    return new_game()


def range1000():
    # Update global range
    global num_range
    num_range = 1000
    return new_game()


def enter(inp):
    # Update global guess field
    global guess
    guess = int(inp)
    input_guess(guess)


# Define other handlers for logic. I think, it's better, for understanding.
# =========================================================================


def num_of_try(value):
    """Numbers of tries."""
    global count
    count = int(math.ceil(math.log(value, 2)))
    return count


# Define Main logic!
# ==================


def input_guess(guess):
    global count
    if guess == secret and count >= 1:
        count -= 1
        print "\nGuess was %d" % guess
        print "Number of remaining guess is %d" % count
        print "Correct! It's Great!"
        return new_game()

    elif guess > secret and count > 1:
        count -= 1
        print "\nGuess was %d" % guess
        print "Number of remaining guess is %d" % count
        print "Lower!"
        return f.add_input

    elif guess < secret and count > 1:
        count -= 1
        print "\nGuess was %d" % guess
        print "Number of remaining guess is %d" % count
        print "Higher!"
        return f.add_input

    elif count <= 1:
        count -= 1
        print "\nGuess was %d" % guess
        print "Number of remaining guess is %d. You Lose. =(" % count
        return new_game()


# Create frame
# ============
f = simplegui.create_frame("Guess the number", 200, 200)


# Register event handlers for control elements
# ============================================
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", enter, 200)


# Call new_game and start frame
# =============================
new_game()
