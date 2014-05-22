# "Stopwatch: The Game"
import simplegui

# define global variables
tic_time = 0
total_stop = 0
sucsess_stop = 0


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    A = t // 600
    B = t // 10 % 60 // 10
    C = t // 10 % 60 % 10
    D = t % 10
    return str(A) + ":" + str(B) + str(C) + "." + str(D)


# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button():
    return timer.start()


def stop_button():
    global total_stop
    global sucsess_stop
    if timer.is_running():
        total_stop += 1
        if tic_time % 10 == 0:
            sucsess_stop += 1
    return timer.stop()


def reset_button():
    global tic_time
    global total_stop
    global sucsess_stop
    tic_time = 0
    total_stop = 0
    sucsess_stop = 0
    return timer.stop()


# define event handler for timer with 0.1 sec interval
def timer_handler():
    global tic_time
    tic_time += 1
    return tic_time


# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(tic_time), (60, 130), 72, 'White')
    canvas.draw_text(str(sucsess_stop) + "/" + str(
                     total_stop), (220, 40), 32, 'Green')

# create frame
frame = simplegui.create_frame('Stopwatch: The Game', 300, 200)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)
frame.add_button('Start', start_button)
frame.add_button('Stop', stop_button)
frame.add_button('Reset', reset_button)

# start frame
frame.start()
