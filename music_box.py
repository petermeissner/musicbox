# imports
from gpiozero import Button

import pygame
import time

import os


def list_dir_recursive(path):
  res = []
  for currentpath, folders, files in os.walk(path):
      for file in files:
          res.append(os.path.join(currentpath, file))
  return res


class Player:
  
  # object state
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




if os.name is not 'nt':
  # initialize player 
  player = Player(music_path = '/home/pi/musicbox/music')

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
  


else:
  
  import pynput
  
  # initialize player 
  player = Player(music_path = 'f:/musicbox/music')

  # key event handler
  def on_press(key):
      global go_on
      print('{0} press'.format(key))

      if key == pynput.keyboard.Key.left:
        player.title_backward()

      if key == pynput.keyboard.Key.right:
        player.title_forward()

      if key == pynput.keyboard.Key.up:
        player.folder_forward()

      if key == pynput.keyboard.Key.down:
        player.folder_backward()

      if key == pynput.keyboard.Key.enter:
        player.play_pause()

      if key == pynput.keyboard.Key.esc:
          # Stop listener
          go_on = False
          return False

  def on_release(key):
      print('{0} release'.format(key))

  listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
  listener.start()
  


# infinit loop and 
print("loop")

go_on = True

while go_on == True:
  if pygame.mixer.music.get_busy() == 0:
    if (player.title_pos + 1) < len(player.title_list):
      player.title_forward()
    time.sleep(1)
  else:
    time.sleep(0.01)


pygame.quit()

