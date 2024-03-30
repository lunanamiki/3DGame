from settings import *
from watcher import *
import random
map_length = map_height
map_width = map_width

TEXTURE_MAPPING = {'.':-1, 'w':0,'D': 1, 'S':2}
#text_map = [''] *map_length 
#for i in range(map_length):
  #for e in range(map_width):
  #  if i == 0 or i == map_length-1 or e == 0 or e == map_width-1:
   #   if random.randint(0,2) == 1:
    #    text_map[i] = text_map[i] + 'w'
    #  else:
    #    text_map[i] = text_map[i] + 'A'
    #else:
   #   if random.randint(0,3) == 1:
   #     text_map[i] = text_map[i] + '.'
   #   else:
   #     text_map[i] = text_map[i] + 'w'
    

#start_index = random.randint(1,map_width-2)
#end_index = random.randint(1,map_width-2)

# text_map[0] = text_map[0][:start_index]+'.'+text_map[0][start_index+1:]
# text_map[map_length-1] = text_map[map_length-1][:end_index]+'.'+text_map[map_length-1][(end_index+1):]

# #pathing agent
# agentx = start_index
# agenty = 1
# iteration = 0
# while agentx != end_index or agenty != map_length-1:
#   iteration += 1
#   if random.randint(0,4) == 1 and agentx > 1:
#    agentx -=1
#   elif random.randint(0,3) == 1 and agentx < map_width-1:
#      agentx +=1
#   elif random.randint(0,2) == 1 and agenty > 1:
#      agenty -=1
#   elif agenty < map_length-1:
#      agenty +=1
  
#   text_map[agenty] = text_map[agenty][:agentx-1] + '.'+ text_map[agenty][agentx:]
#   for row in text_map:
#     print(row)
 # print("iteration" + str(iteration))
text_map = [['w' for _ in range(map_width)] for _ in range(map_length)]
player_start_pos = (0,0)
enemy_start_pos = (0,0)
world_map = []
start_x = 0


def generate_maze(x,y):
  directions = [(0,1), (0,-1),(1,0),(-1,0)]
  random.shuffle(directions)
  for dx, dy in directions:
    new_x, new_y = x+dx * 2, y+dy *2
    if 0 <= new_x < map_width and 0 <= new_y < map_length and text_map[new_y][new_x] == 'w':
      text_map[y+ dy][x+dx]='.'
      text_map[new_y][new_x] = '.'
      generate_maze(new_x, new_y)

def final_generation():
  halfx = int(map_width//2)
  halfy = int(map_length//2)

  xindex = random.randrange(0, map_width//2)*2
  yindex = random.randrange(0, map_length//2)*2+1
  if 0 < xindex < map_width and 0 < yindex < map_length and text_map[yindex][xindex] == 'w':
    text_map[yindex][xindex] = '.'
    print("Cleared:" +str(yindex)+", "+str(xindex))
  else:
    final_generation()

def generate_level(w,l):
  global player_start_pos, enemy_start_pos, text_map, world_map, map_width, map_length, start_x
  print("MAP:"+str(l) + "," + str(w))
  map_length = l
  map_width = w
  text_map = [['w' for _ in range(map_width)] for _ in range(map_length)]
  start_x, start_y = random.randrange(1, map_width,2), random.randrange(1, map_length,2)
  generate_maze(start_x, start_y)
  

  text_map[0][start_x]= 'S'
  end_x = random.randrange(1, map_width - 1, 2)
  text_map[map_length -1][end_x] = 'D'
  
  player_start_pos = ((start_x)*100 +50, 150)
  enemy_start_pos = ((end_x)*100+50, (map_length-1)*100-50)

  final_generation()
  final_generation()
  final_generation()

  for row in text_map:
    print(row)
  world_map = set()
  for j, row in enumerate(text_map):
    for i, char in enumerate(row):
      if char != '.':
        if char in TEXTURE_MAPPING:
          world_map.add((i * TILE, j * TILE, TEXTURE_MAPPING[char]))

def getplayerpos():
  global player_start_pos
  return player_start_pos

def getenemypos():
  global enemy_start_pos
  return enemy_start_pos

def getworldmap():
  global world_map
  return world_map

#text_map = [
 # 'wwwwww.wwwwww',
  #'w..........w',
 # 'w...wwww...w',
  #'w...w......w',
  #'w..........w',
  #'w....www...w',
  #'w..........w',
 # 'wwwwwwww.wwww'
#]




def get_texture_index(x,y):
  global world_map
  for item in world_map:
    if item[0] == x and item[1] == y:
      return item[2]
  return TEXTURE_MAPPING['.']