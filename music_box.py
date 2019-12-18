# imports
from gpiozero import Button
import pygame

pygame.init()

# initialize button
btn17 = Button(17)
btn27 = Button(27)
btn22 = Button(22)
btn23 = Button(23)
btn24 = Button(24)

# initialize music player state
pygame.mixer.init()
pygame.mixer.music.load('/home/pi/musicbox/music.mp3')
pygame.mixer.music.play()
pygame.mixer.music.pause()
play_state = "pause"


def h27():
    # tell function its ok to use global variable
    global play_state

    if pygame.mixer.music.get_busy() == 0:
        print("dings")
        pygame.mixer.music.play()
        pygame.mixer.music.unpause()
        play_state = "unpause"
    else:
        if play_state == "pause":
            pygame.mixer.music.unpause()
            play_state = "unpause"

        elif play_state == "unpause":
            pygame.mixer.music.pause()
            play_state = "pause"

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
btn27.when_pressed = h27
btn22.when_pressed = h22
btn23.when_pressed = h23
btn24.when_pressed = h24
