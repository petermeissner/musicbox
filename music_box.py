# imports
from gpiozero import Button
import pygame

from signal import pause

import os


class Player:
  
  dir_list   = []
  dir_pos    = 0
  
  title_list = []
  title_pos  = 0

  play_state = "pause"
  music_path  = '.'

  # Initialize
  def __init__(self, music_path):
    
    self.music_path = music_path

    self.refresh_dir_list()
    self.refresh_title_list()

    # initialize music player state
    pygame.mixer.init()
    pygame.mixer.music.load(self.title_list[self.title_pos])
    pygame.mixer.music.play()
    pygame.mixer.music.pause()

    self.info("-- player ready -- ")

  def refresh_title_list(self):
    self.title_pos = 0
    pth = os.path.join(self.dir_list[self.dir_pos])
    self.title_list = [os.path.join(pth, f) for f in os.listdir(pth) if os.path.isfile(os.path.join(pth, f))]
    self.title_list = [ fi for fi in self.title_list if fi.endswith(".mp3") ]
    self.title_list.sort()

  def refresh_dir_list(self):
    pth = self.music_path
    self.dir_list = [os.path.join(pth, f)  for f in os.listdir(pth) if os.path.isdir(os.path.join(pth, f))]
    self.dir_list.sort()

  def info(self, pre):
    print(pre, self.dir_pos, self.dir_list[self.dir_pos], self.title_pos, self.title_list[self.title_pos])


  def folder_forward(self):
    self.refresh_dir_list()
    new_pos = min(len(self.dir_list) - 1, self.dir_pos + 1)

    if new_pos is not self.dir_pos:
      self.dir_pos = new_pos
      self.refresh_title_list()
      self.play_current_title_item()

    self.info(">>")


  def folder_backward(self):
    self.refresh_dir_list()
    new_pos = max(0, self.dir_pos - 1)

    if new_pos is not self.dir_pos:
      self.dir_pos = new_pos
      self.refresh_title_list()
      self.play_current_title_item()

    self.info("<<")


  def title_forward(self):
    new_pos = min(len(self.title_list) - 1 , self.title_pos + 1)

    if new_pos is not self.title_pos:
      self.title_pos = new_pos
      self.play_current_title_item()

    self.info("|>")
  

  def title_backward(self):
    new_pos = max(0, self.title_pos - 1)
    
    if new_pos is not self.title_pos:
      self.title_pos = new_pos
      self.play_current_title_item()

    self.info("<|")


  def play_current_title_item(self):
    pygame.mixer.music.load(self.title_list[self.title_pos])
    pygame.mixer.music.play()
    pygame.mixer.music.unpause()
    self.play_state = "unpause"



  def play_pause(self):

    # check if maybe player is done playing or not
    if pygame.mixer.music.get_busy() == 0:
        # if player is done restart current title and unpause

        pygame.mixer.music.play()
        pygame.mixer.music.unpause()
        self.play_state = "unpause"

    else:
        # if player still has some title to play switch pause state

        # pause --> unpause
        if self.play_state == "pause":
            pygame.mixer.music.unpause()
            self.play_state = "unpause"

        # unpause --> pause
        elif self.play_state == "unpause":
            pygame.mixer.music.pause()
            self.play_state = "pause"

    # print some feedback to console
    if self.play_state == "pause":
      self.info("||")
    else:
      self.info("~~")


# initialize pygame module
import pygame.display
os.putenv('SDL_VIDEODRIVER', 'fbcon')
pygame.display.init()
pygame.init()

# add nwe event to pygame machinery
MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)


# initialize button
play_pause_btn      = Button(23)
title_forward_btn   = Button(22)
title_backward_btn  = Button(27)
folder_forward_btn  = Button(24)
folder_backward_btn = Button(17)


# initilize player 
player = Player(music_path = '/home/pi/musicbox/music')


# wire up buttons and player functions
play_pause_btn.when_pressed      = player.play_pause
title_forward_btn.when_pressed   = player.title_forward
title_backward_btn.when_pressed  = player.title_backward
folder_forward_btn.when_pressed  = player.folder_forward
folder_backward_btn.when_pressed = player.folder_backward


# keep script running 
#pause()

go_on = True
while go_on == True:
  for event in pygame.event.get():
    
    if event.type == MUSIC_END:
      player.title_forward()


pygame.quit()

