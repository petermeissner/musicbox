# imports
from gpiozero import Button
import pygame

from signal import pause


# initialize pygame module
pygame.init()

# initialize button
play_pause_btn = Button(27)
btn17 = Button(17)
btn22 = Button(22)
btn23 = Button(23)
btn24 = Button(24)

# initialize music player state
pygame.mixer.init()
pygame.mixer.music.load('/home/pi/musicbox/file-examples.com-music.mp3')
pygame.mixer.music.play()
pygame.mixer.music.pause()
play_state = "pause"


# play/pause event function
def play_pause_func():
    # tell function its ok to use global variable
    global play_state

    # check if maybe player is done playing or not
    if pygame.mixer.music.get_busy() == 0:
        # if player is done restart current title and unpause

        pygame.mixer.music.play()
        pygame.mixer.music.unpause()
        play_state = "unpause"

    else:
        # if player still has some title to play switch pause state

        # pause --> unpause
        if play_state == "pause":
            pygame.mixer.music.unpause()
            play_state = "unpause"

        # unpause --> pause
        elif play_state == "unpause":
            pygame.mixer.music.pause()
            play_state = "pause"

    # print some feedback to console
    print("27 " + play_state)



def h17():
    print("17")

def h22():
    print("22")

def h23():
    print("23")

def h24():
    print("24")

btn17.when_pressed = h17
play_pause_btn.when_pressed = play_pause_func
btn22.when_pressed = h22
btn23.when_pressed = h23
btn24.when_pressed = h24


# keep script running 
pause()
