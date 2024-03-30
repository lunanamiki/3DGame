
from settings import *
from watcher import *
from queue import PriorityQueue
import math, pygame
from map import world_map, get_texture_index, enemy_start_pos, getenemypos



class Enemy:
  def __init__(self):
    self.x,self.y = getenemypos()
    self.size = 50
    self.angle = enemy_angle
    self.path = []

  @property
  def pos(self):
    return (self.x, self.y)
  
  @property
  def getpath(self):
    return self.path

  def movement(self, playerx, playery, map_w,map_l):
    self.path = self.find_path(playerx, playery, map_w,map_l)
    if len(self.path) == 0:
      self.move_towards(playerx,playery)
    if self.path:
      self.follow_path(self.path)

  

  def follow_path(self, path):
    if path:
      next_tile = path.pop(0)
      next_x, next_y = next_tile[0] * TILE + TILE //2,next_tile[1] * TILE + TILE //2
      self.move_towards(next_x,next_y)

  def move_towards(self, target_x, target_y):
    xdif = target_x - self.x
    ydif = target_y - self.y
    angle = math.atan2(ydif, xdif)
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)

    self.x += enemy_speed * cos_a
    self.y += enemy_speed * sin_a

  def resetpos(self):
    self.x,self.y = getenemypos()

  def find_path(self, playerx, playery, map_w, map_l):
    start = (int(self.x // TILE), int(self.y // TILE))
    end = (int(playerx // TILE), int(playery //TILE))

    open_set = PriorityQueue()
    open_set.put(start, 0)

    came_from = {}
    g_score = {start:0}

    while not open_set.empty():
      current = open_set.get()

      if current == end:
        path = []
        while current in came_from:
          path.append(current)
          current = came_from[current]
        path.reverse()
        return path
      for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
        neighbor = (current[0]+dx, current[1]+dy)
        new_g_score = g_score[current]+1
        if 0 <= neighbor[0] and neighbor[0]< map_w and 0<= neighbor[1] and neighbor[1]< map_l:
          texture_index = get_texture_index(neighbor[0] * TILE, neighbor[1] * TILE)
          if texture_index != 0 and (neighbor not in g_score or new_g_score < g_score[neighbor]):
            g_score[neighbor] = new_g_score
            priority = new_g_score + self.heuristic(neighbor, end)
            open_set.put(neighbor,priority)
            came_from[neighbor] = current

    return None

  def heuristic(self, a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
