import pygame, math
from watcher import *
from settings import *
from map import world_map, get_texture_index, getworldmap

endGame = False

textures = [
  pygame.image.load('brick.png'),
  pygame.image.load('pink.png'),
  pygame.image.load('pink.png')
]
enemytexture = pygame.image.load('enemytexture.png')


def getEndGame():
  return endGame


def ray_casting(sc, player_pos, player_angle, enemy):
  global endGame
  cur_angle = player_angle - HALF_FOV
  xo, yo = player_pos

  hasHitEnemy = False
  for ray in range(NUM_RAYS):

    cos_a = math.cos(cur_angle)
    sin_a = math.sin(cur_angle) 
    for depth in range(MAX_DEPTH):
      x = xo + depth * cos_a
      y = yo + depth * sin_a
      map_x, map_y = x // TILE * TILE, y // TILE * TILE
      #pygame.draw.line(sc, DARKGREY, player_pos, (x,y), 2)

      texture_index = get_texture_index(map_x, map_y)
      if (not hasHitEnemy and x < enemy.x + enemy.size / 2
          and x > enemy.x - enemy.size / 2 and y < enemy.y + enemy.size / 2
          and y > enemy.y - enemy.size / 2):
        proj_height = 1
        hasHitEnemy = True

        proj_size = depth / MAX_DEPTH
        if math.dist([xo,yo],[enemy.x,enemy.y]) < enemy.size/2:
          endGame = True 
        elif depth == 0:
          endGame = True
        else:
          proj_height = PROJ_COEFF / depth
          if proj_height > 800:
            proj_height = 800
        #lastval = [(x-cos_a),(y-sin_a)]
        #if lastval[0] < enemy.x-enemy.size/2 or lastval[0] > enemy.x+enemy.size/2:
        #coordinate = int(int(y-(enemy.y-(enemy.size/2)))*(TEXTURE_SCALE/enemy.size))
        #else:
        #  coordinate = int(int(x-(enemy.x-(enemy.size/2)))*(TEXTURE_SCALE/enemy.size))

        #print(coordinate)
        #scarledtexture = enemytexture.subsurface((coordinate, 0, 1, enemytexture.get_height()))
        #slicedtexture = pygame.transform.scale(scarledtexture, (SCALE, int(proj_height)))
        scaledtexture = pygame.transform.scale(
          enemytexture, (int(proj_height), int(proj_height)))
        sc.blit(scaledtexture, (ray * SCALE, HALF_HEIGHT - proj_height // 2))

      #pygame.draw.line(sc, DARKGREY, player_pos, (x,y), 2)
      if (map_x, map_y, texture_index) in getworldmap():
        coordinate = 0
        lastval = [(x - cos_a) // TILE * TILE, (y - sin_a) // TILE * TILE]
        if lastval[0] < map_x or lastval[0] > map_x:
          coordinate = int(int(y) % (TEXTURE_SCALE))
        else:
          coordinate = int(int(x) % (TEXTURE_SCALE))

        #print(texture_x)
        wall_column = textures[texture_index].subsurface(
          (coordinate, 0, 1, textures[texture_index].get_height()))
        
        proj_height = 1
        if depth == 0:
          print("In wall?")
        else:
          proj_height = PROJ_COEFF / depth

        darkness_factor = 1 - (depth / MAX_DEPTH)
        wall_column.set_alpha(int(darkness_factor * DARKNESS * 255))

        wall_slice = pygame.transform.scale(wall_column,
                                            (SCALE, int(proj_height)))
        sc.blit(wall_slice, (ray * SCALE, HALF_HEIGHT - proj_height // 2))
        break

    cur_angle += DELTA_ANGLE