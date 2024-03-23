
from settings import *
import math, pygame 
from map import world_map, player_start_pos, get_texture_index, generate_level,getplayerpos, getworldmap

class Player:
  def __init__(self):
    self.x,self.y = getplayerpos()
    self.angle = player_angle
    self.awaitingGeneration = False

  @property
  def pos(self):
    return (self.x, self.y)

  def isGenerating(self):
    if self.awaitingGeneration:
      self.awaitingGeneration = False
      print("Awaitinh True! Set: " +str(self.awaitingGeneration))
      return True
    else:
      return False

  def movement(self):
    cos_a = math.cos(self.angle)
    sin_a = math.sin(self.angle)
    
    nextx = self.x
    nexty = self.y
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
      nextx += player_speed * cos_a
      nexty += player_speed * sin_a
      
    if keys[pygame.K_s]:
      nextx -= player_speed * cos_a
      nexty -= player_speed * sin_a
      
    if keys[pygame.K_a]:
      nextx += player_speed * sin_a
      nexty += -player_speed * cos_a
      
    if keys[pygame.K_d]:
      nextx += -player_speed * sin_a
      nexty += player_speed * cos_a
    
    nextxtile = nextx // TILE* TILE
    nextytile = nexty // TILE * TILE
    
    texture_index = get_texture_index(nextxtile, nextytile)
    if not(nextxtile, self.y // TILE * TILE, texture_index) in getworldmap():
      self.x = nextx
    elif texture_index == 1:
      generate_level()
      self.awaitingGeneration = True
      self.x,self.y = getplayerpos()

  
   
      
    if not(self.x // TILE * TILE, nextytile, texture_index) in getworldmap():
      self.y = nexty
    elif texture_index == 1:
      generate_level()
      self.awaitingGeneration = True
      self.x,self.y = getplayerpos()
      
    if keys[pygame.K_LEFT]:
      self.angle -= .01 * player_speed
      
    if keys[pygame.K_RIGHT]:
      self.angle += .01 * player_speed