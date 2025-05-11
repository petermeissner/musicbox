#### Description #### ----------------------------------------------------------

# Simple MP3 Music-Player 
# 
# Uses pygame for event handling and mp3 playing
#
# 5 physical Buttons are used for control
#
# 1)  <<- folder backward = Pin 17
# 2)  <-- title backward  = Pin 27
# 3)  |>  play pause      = Pin 23
# 4)  --> title forward   = Pin 22
# 5)  ->> folder forward  = Pin 24
#  


#### Imports ####
from gpiozero import Button

import pygame

import datetime
import time
import os

from typing import List





#### Functions #### ------------------------------------------------------------

def list_dir_recursive(path: str) -> List[str]:
  """
  Goes through folder and lists all its files. 

  Args:
      path (str): path to look for files

  Returns:
      List[str]: a list of file paths
  """
  res = []
  for currentpath, folders, files in os.walk(path):
      for file in files:
          res.append(os.path.join(currentpath, file))
  return res




#### Classes #### --------------------------------------------------------------
class Player:
  """
  Class that serves as a music player connecting button events to play actions
  depending on the current state - e.g. play/pause, current track, current folder. 
  """


  # object states
    
  # - current directory
  dir_list   = []
  dir_pos    = 0
  
  # - current title
  title_list = []
  title_pos  = 0
  
  # - current play state
  play_state = "pause"

  # - optional musicpath
  music_path  = '.'

  
  
  # - option for minumum time between button presses
  time_between_presses = 0.3
  # timestamp for last button press (or initialization time at start)
  last_press = time.time()



  
  # check if time between button presses is ok
  def check_press(self):
    """
    Method for checking if time between button presses is ok.
    """
    if (time.time() - self.last_press) < self.time_between_presses:
      return False
    else:
      self.last_press = time.time()
      return True

  def music_load(self, path: str):
    """
    Method for loading a new mp3 file.

    Args:
        path (str): path to mp3 file
    """
    pygame.mixer.music.load(path)


  # Initialize
  def __init__(self, music_path: str):

    # store musicpath 
    self.music_path = music_path

    # read in directories and titles in music path
    self.refresh_dir_list()
    self.refresh_title_list()

    print("dir_list: ", self.dir_list)
    print("title_list: ", self.title_list)

    # initialize music player state with first track and a ready music player
    pygame.mixer.init()

    # play startup message
    print("playing startup message")
    self.music_load("musikbox-gestartet.mp3")
    pygame.mixer.music.play()
    time.sleep(2)
    print("playing startup message - done")
    pygame.mixer.music.pause()

    # play first track
    self.music_load(self.title_list[self.title_pos])
    pygame.mixer.music.play()
    pygame.mixer.music.pause()

    self.info("-- player ready -- ")



  def refresh_title_list(self):
    """
    Method for re-initializing title list: re-set position + re-list titles in folder
    """

    # reset title position
    self.title_pos = 0
    
    # list files
    self.title_list = list_dir_recursive(self.dir_list[self.dir_pos])
    
    # filter
    self.title_list = [ fi for fi in self.title_list if fi.endswith(".mp3") ]
    
    # sort 
    self.title_list.sort()

    # handle empty folders
    if len(self.title_list) == 0:
      self.title_list = self.music_path.join("/keine-titel-gefunden.mp3")



  def refresh_dir_list(self):
    """
    Method for refreshing the current list of folders.
    """

    pth = self.music_path
    self.dir_list = [os.path.join(pth, f)  for f in os.listdir(pth) if os.path.isdir(os.path.join(pth, f))]
    self.dir_list.sort()



  def info(self, pre: str):
    """
    Method for printing info about current player state.

    Args:
        pre (str): A string prefix, to be printed before
    """
    print(
      pre, 
      "; dir_pos: ", self.dir_pos, 
      "; dir: ", self.dir_list[self.dir_pos], 
      "; title_pos: ", self.title_pos, 
      "; title: ", self.title_list[self.title_pos]
    )



  def folder_forward(self):
    """
    Method for acting on folder-forward button push: going to next folder in list
    """
    # check if time between button presses is ok
    if not self.check_press():
      return
    
    self.refresh_dir_list()
    new_pos = min(len(self.dir_list) - 1, self.dir_pos + 1)

    if new_pos is not self.dir_pos:
      self.dir_pos = new_pos
      self.refresh_title_list()
      self.play_current_title_item()

    self.info(">>")



  def folder_backward(self):
    """
    Method for acting on folder-backward button push: going to previous folder in list
    """
    # check if time between button presses is ok
    if not self.check_press():
      return
    
    self.refresh_dir_list()
    new_pos = max(0, self.dir_pos - 1)

    if new_pos is not self.dir_pos:
      self.dir_pos = new_pos
      self.refresh_title_list()
      self.play_current_title_item()

    self.info("<<")



  def title_forward(self):
    """
    Method for acting on title-forward button push: going to next title in list
    """
    # check if time between button presses is ok
    if not self.check_press():
      return

    new_pos = min(len(self.title_list) - 1 , self.title_pos + 1)

    if new_pos is not self.title_pos:
      self.title_pos = new_pos
      self.play_current_title_item()

    self.info("->")
  

  def title_backward(self):
    """
    Method for acting on title-backward button push: going to previous title in list
    """
    # check if time between button presses is ok
    if not self.check_press():
      return
    
    new_pos = max(0, self.title_pos - 1)
    
    if new_pos is not self.title_pos:
      self.title_pos = new_pos
      self.play_current_title_item()

    self.info("<-")


  def play_current_title_item(self):
    """
    Method for playing current title.
    """
    self.music_load(self.title_list[self.title_pos])
    pygame.mixer.music.play()
    pygame.mixer.music.unpause()
    self.play_state = "unpause"



  def play_pause(self):
    """
    Method alternating between play and pause.
    """
    # check if time between button presses is ok
    if not self.check_press():
      self.info("X button press ignored, too fast --")
      return

    # pause --> unpause
    if self.play_state == "pause":
        self.info("|>")
        pygame.mixer.music.unpause()
        self.play_state = "unpause"

    # unpause --> pause
    elif self.play_state == "unpause":
        self.info("||")
        pygame.mixer.music.pause()
        self.play_state = "pause"



 #### DoingDutyToDo #### -------------------------------------------------------


# initialize player 
player = Player(music_path = '/home/musicpi/musicbox/music')

# initialize buttons
play_pause_btn      = Button(23)
title_forward_btn   = Button(22)
title_backward_btn  = Button(27)
folder_forward_btn  = Button(24)
folder_backward_btn = Button(17)

# wire up buttons and player functions
play_pause_btn.when_pressed      = player.play_pause
title_forward_btn.when_pressed   = player.title_forward
title_backward_btn.when_pressed  = player.title_backward
folder_forward_btn.when_pressed  = player.folder_forward
folder_backward_btn.when_pressed = player.folder_backward

print("loop")
go_on = True
while go_on == True:
  
  # if player is idle, play next track
  not_busy = pygame.mixer.music.get_busy() == 0
  should_play = player.play_state == "unpause" 

  if not_busy and should_play:
    if (player.title_pos + 1) < len(player.title_list):
      player.title_forward()
    time.sleep(1)
  
  # if busy, just wait a little bit and check again
  else:
    time.sleep(0.2)



# tear down and exit
pygame.quit()

