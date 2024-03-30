import pygame, sys, math, random
from settings import *
from player import Player
from enemy import Enemy
from map import world_map, player_start_pos, generate_level, getworldmap
from pygame.locals import QUIT
from ray_casting import ray_casting, getEndGame

### CIRCULAR IMPORTERROR::: 
### Main imports watcher which imports something that main depends upon
###         main < -----------------
###           |                         |
###           V                         |
###         watcher.py    ------>     map.py

pygame.init()

running = True
generateNewLevel = False
levelCounter = 1
sc = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
generate_level(map_width,map_height)
player = Player()
enemy = Enemy()
pygame.display.set_caption('3D GAME')
font = pygame.font.Font('freesansbold.ttf', 32)
def reset_enemy_pos():
  global enemy
  enemy.resetpos()

# dear landon, it seems that get_new_gen() is a fancier way of simply saying "return False"
# we say that (if get_new_gen() == True:) inside of our watcher.py, but that will always be false,
# resulting in our code not running
INT_HEIGHT = map_height
INT_WIDTH = map_width

while True:
   
   for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
      
   player.movement()
   enemy.movement(player.x, player.y, INT_WIDTH, INT_HEIGHT)
   

   if player.isGenerating():
     INT_WIDTH = random.randrange(11+((levelCounter-1)*2),14+((levelCounter-1)*2),2)
     INT_HEIGHT = random.randrange(11+((levelCounter-1)*2),14+((levelCounter-1)*2),2)
     print("WATCHER:"+str(INT_HEIGHT) + "," + str(INT_WIDTH))
   
     generateNewLevel = True
     levelCounter += 1
     generate_level(INT_WIDTH,INT_HEIGHT)
     reset_enemy_pos()
     
   sc.fill(BLACK)
   ray_casting(sc, player.pos, player.angle, enemy)
  
   pygame.draw.circle(sc, GREEN, (int(player.x), int(player.y)) ,12)
   pygame.draw.circle(sc, RED, (int(enemy.x), int(enemy.y)) ,12)
   #pygame.draw.line(sc, RED, enemy.pos, (enemy.x + WIDTH * math.cos(enemy.angle),enemy.y + HEIGHT * math.sin(enemy.angle)))
   pygame.draw.line(sc, GREEN, player.pos, (player.x + WIDTH * math.cos(player.angle),player.y + HEIGHT * math.sin(player.angle)))

   for x, y, t in getworldmap():
    pygame.draw.rect(sc,DARKGREY, (x, y, TILE, TILE), 2)

   
   text = font.render("Level "+str(levelCounter), True, (255,255,255))
   textRect = text.get_rect()
   textRect.center = (WIDTH/2, 30)
   sc.blit(text,textRect)
   if getEndGame():
    gameOverText = font.render("GAME OVER", True, (255,0,0))
    gameOverRect = gameOverText.get_rect()
    gameOverRect.center = (600, 400)
    sc.blit(gameOverText, gameOverRect)
    
     


   clock.tick(FPS)
   pygame.display.update()

   if getEndGame():
     pygame.time.delay(3000)
     pygame.quit()
     quit()
     # commented out by painter on 2024-03-16
     #running = False

