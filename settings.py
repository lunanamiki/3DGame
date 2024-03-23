import math
import random


#game settings
TILE = 100
map_width = 11
map_height = 11
WIDTH = 1200
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

#player settings
player_pos = (HALF_WIDTH, HALF_HEIGHT)
player_angle = 0
player_speed = 10
FPS= 30

#enemy settings
enemy_angle = 0
enemy_speed = 5

#recasting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 40
MAX_DEPTH = 700
DELTA_ANGLE = FOV /NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 20 * DIST * TILE
SCALE = WIDTH // NUM_RAYS
DARKNESS = .8
TEXTURE_SCALE = 100

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (220, 0, 0)
GREEN = (0, 220, 0)
BLUE =(0,0,220)
DARKGREY = (110,110,110)
PURPLE = (120,0,120)

def generateLevelSettings(level):
 global INT_WIDTH, INT_HEIGHT
 INT_WIDTH = random.randrange(11+((level-1)*2),14+((level-1)*2),2)
 INT_HEIGHT = random.randrange(11+((level-1)*2),14+((level-1)*2),2)
 print("SETTINGS:"+str(INT_HEIGHT) + "," + str(INT_WIDTH))