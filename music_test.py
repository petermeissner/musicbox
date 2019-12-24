# imports
from gpiozero import Button
import pygame

from signal import pause

import os




# initialize button
play_pause_btn      = Button(23)
title_forward_btn   = Button(22)
title_backward_btn  = Button(27)
folder_forward_btn  = Button(24)
folder_backward_btn = Button(17)




# wire up buttons and player functions
play_pause_btn.when_pressed      = lambda : print(23, "~~")
title_forward_btn.when_pressed   = lambda : print(22, "->")
title_backward_btn.when_pressed  = lambda : print(27, "<-")
folder_forward_btn.when_pressed  = lambda : print(24, ">>")
folder_backward_btn.when_pressed = lambda : print(17, "<<")


# keep script running 
pause()


