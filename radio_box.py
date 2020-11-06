# packages
import os
from pathlib import Path

from omxplayer.player import OMXPlayer
from gpiozero import Button




# # classes 
# class Player:
  
#   pause: bool = True
#   process: Popen = None

  # url_list = [
  #   'https://st02.sslstream.dlf.de/dlf/02/128/mp3/stream.mp3'
  # ]
  # url_pos: int = 0

#   def __init__(self) -> None:
#     self.play_pause()

#   def __del__(self):
#     os.killpg(os.getpgid(self.process.pid), 15)

#   def play_pause(self):
#     print("..Pause: ", self.pause)

#     if self.pause:
#       print("... play")
#       self.process = Popen(['omxplayer', self.url_list[self.url_pos]], 
#                       stdout=PIPE, 
#                       stderr=PIPE,
#                       preexec_fn=os.setsid)
#       self.pause = False

#     else:
#       print("... kill", self.process.pid)
#       os.killpg(os.getpgid(self.process.pid), 15)

#       self.pause = True


#   def title_forward(self):
#     print("Forward")

#   def title_backward(self):
#     print("Backward")

#   def folder_forward(self):
#     print("Folder Forward")
  
#   def folder_backward(self):
#     print("Folder Backward")
  

# player = Player()


# # initialize buttons
# play_pause_btn      = Button(23)
# title_forward_btn   = Button(22)
# title_backward_btn  = Button(27)
# folder_forward_btn  = Button(24)
# folder_backward_btn = Button(17)

# # wire up buttons and player functions
# play_pause_btn.when_pressed      = player.play_pause
# title_forward_btn.when_pressed   = player.title_forward
# title_backward_btn.when_pressed  = player.title_backward
# folder_forward_btn.when_pressed  = player.folder_forward
# folder_backward_btn.when_pressed = player.folder_backward


# while True:
#   time.sleep(0.1)


from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep


url_list = [
  'https://st02.sslstream.dlf.de/dlf/02/128/mp3/stream.mp3',
  'https://radio.toggo.de/live/mp3-192'
]
url_pos: int = 0

player = OMXPlayer('keine-titel-gefunden.mp3')


try:
  player.load(url_list[url_pos])
except:
  sleep(5)
  player.load(url_list[url_pos])


  


# sleep(5)
# player.quit()

# player = OMXPlayer(url_list[url_pos+1])
# sleep(5)
# player.quit()
