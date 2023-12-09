from platform import platform
import pygame 
import time 
import random 
from map import *

pygame.init()

#IMAGES
bgimage=pygame.image.load("images/bg_sky.png") 
ledgeimage=pygame.image.load("images/ledge.png") 
lavaimage=pygame.image.load("images/lava.jpg") 
cactusimage=pygame.image.load("images/cactus_4.png")
font = pygame.font.Font('freesansbold.ttf', 32)
#CONSTANTS
WIDTH,HEIGHT=1273,728
TILE_SIZE=17
timer1=0
 
lava_group=pygame.sprite.Group()
cactus_group=pygame.sprite.Group()
platform_group = pygame.sprite.Group()
health_group=pygame.sprite.Group()
pipe_group=pygame.sprite.Group()
water_group=pygame.sprite.Group()
ball_group=pygame.sprite.Group()
rope_group=pygame.sprite.Group()
rope_group2=pygame.sprite.Group()
soil_group=pygame.sprite.Group()

#GAME
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock() 
rocks=[]

class World:
    def __init__(self,data):
        self.tile_list=[]  
         
        row_num=0
        for row in data:
            col_num=0
            for col in row: 
                if col==1:
                    ledgeimage=pygame.image.load("images/stone.jpg")
                    ledgeimage=pygame.transform.scale(ledgeimage,(17,17))
                    rect=ledgeimage.get_rect()
                    rect.x=col_num*TILE_SIZE
                    rect.y=row_num*TILE_SIZE
                    block=(ledgeimage,rect)
                    self.tile_list.append(block)
                if col == 12:
                    platform = Platform(col_num * TILE_SIZE, row_num * TILE_SIZE, 0, 1)
                    platform_group.add(platform)
                if col==3:
                    lava=Lava(col_num * TILE_SIZE,row_num * TILE_SIZE)
                    lava_group.add(lava)
                if col==13:
                    cactus=Cactus(col_num * TILE_SIZE,row_num * TILE_SIZE)
                    cactus_group.add(cactus)
                if col==5:
                    health=Health(col_num * TILE_SIZE,row_num * TILE_SIZE)
                    health_group.add(health)
                if col==6:
                    pipe=Pipe(col_num * TILE_SIZE,row_num * TILE_SIZE,90)
                    pipe_group.add(pipe)
                if col==7:
                    pipe=Pipe(col_num * TILE_SIZE,row_num * TILE_SIZE,180)
                    pipe_group.add(pipe)
                if col==8:
                    water=Water(col_num * TILE_SIZE,row_num * TILE_SIZE)
                    water_group.add(water)
                if col==9:
                    ball=Ball(col_num * TILE_SIZE,row_num * TILE_SIZE*(99/100))
                    ball_group.add(ball)
                if col==10:
                    rope=Rope(col_num * TILE_SIZE,row_num * TILE_SIZE,movement=True)
                    rope_group.add(rope)
                if col==11:
                    rope=Rope(col_num * TILE_SIZE,row_num * TILE_SIZE,movement=False)
                    rope_group2.add(rope)
                if col==2:
                    soilimage=pygame.image.load("images/soil.png")
                    soilimage=pygame.transform.scale(soilimage,(TILE_SIZE,TILE_SIZE))
                    rect=soilimage.get_rect()
                    rect.x=col_num*TILE_SIZE
                    rect.y=row_num*TILE_SIZE
                    block=(soilimage,rect)
                    self.tile_list.append(block)
                if col==4:
                    obsidianimage=pygame.image.load("images/obsidian.jpg")
                    obsidianimage=pygame.transform.scale(obsidianimage,(TILE_SIZE,TILE_SIZE))
                    rect=obsidianimage.get_rect()
                    rect.x=col_num*TILE_SIZE
                    rect.y=row_num*TILE_SIZE
                    block=(obsidianimage,rect)
                    self.tile_list.append(block)
                
                col_num+=1
            row_num+=1

    def draw(self):
        for tile in self.tile_list:
             
            screen.blit(tile[0],tile[1])

class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("images/lava.jpg")
        self.image=pygame.transform.scale(self.image,(TILE_SIZE*2,TILE_SIZE*2))
        self.rect=self.image.get_rect(topleft=(x,y))
        self.mask=pygame.mask.from_surface(self.image)

class Water(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("images/water.jpg")
        self.image=pygame.transform.scale(self.image,(TILE_SIZE*2,TILE_SIZE*2))
        self.rect=self.image.get_rect(topleft=(x,y))
        self.mask=pygame.mask.from_surface(self.image)

class Cactus(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("images/cactus_4.png")
        self.image=pygame.transform.scale(self.image,(TILE_SIZE*2,TILE_SIZE*4))
        self.rect=self.image.get_rect(topleft=(x,y))
        self.mask=pygame.mask.from_surface(self.image)

class Swing:
    def __init__(self,m,n):
        self.image=pygame.image.load("images/p1.png")
        self.image=pygame.transform.scale(self.image,(90*4/5,34*3/5))
        self.rect=self.image.get_rect()
        self.rect.x=m*TILE_SIZE  #49
        self.rect.y=n*TILE_SIZE   #37
        self.mask=pygame.mask.from_surface(self.image)
        self.swing_rotated=False
        self.finished=False
        self.timer1=0
    def update(self):
        screen.blit(self.image,self.rect)
        if player.health<=0:
            self.rect.x=49*17
            self.rect.y=37*17
         
        if player.rect.colliderect(self.rect):
             
            player.dy=0
            # player.vely=0
            
            if player.rect.x<self.rect.x+self.image.get_width()/2:
                player.canjump=True
                if self.swing_rotated==False:
                    if self.finished==False:
                        self.image=pygame.transform.rotate(self.image,10)
                             
                
            if self.rect.x+self.image.get_width()/2<player.rect.x<self.rect.x+self.image.get_width():
                player.canjump=True
                if self.swing_rotated==False:
                    if self.finished==False:
                        self.image=pygame.transform.rotate(self.image,-10)
                        self.swing_rotated=True

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        #pygame.sprite.Sprite.__init__(self)
        super().__init__()
        img = pygame.image.load('images/p1.png')
        self.image = pygame.transform.scale(img, (TILE_SIZE*4, TILE_SIZE ))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask=pygame.mask.from_surface(self.image)
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y
    def update(self):
        
        if player.rect.x<600 and player.rect.y>500:
            self.rect.x += self.move_direction * self.move_x
            self.rect.y += self.move_direction * self.move_y
            self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
    
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,angle):
        super().__init__()
        self.image=pygame.image.load("images/pipe.png")
        self.image=pygame.transform.rotate(self.image,angle)
        self.image=pygame.transform.scale(self.image,(TILE_SIZE*2,TILE_SIZE*2))
        self.rect=self.image.get_rect(topleft=(x,y))
        self.mask=pygame.mask.from_surface(self.image)

class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("images/ball1.png")
        self.image=pygame.transform.scale(self.image,(TILE_SIZE*4,TILE_SIZE*4))
        self.rect=self.image.get_rect(topleft=(x,y))
        self.mask=pygame.mask.from_surface(self.image)
        self.direction=1
        self.velx=2
        self.movecounter=0
    def update(self):
        self.rect.x+=self.direction*self.velx
         
        self.movecounter+=1
        if abs(self.movecounter)>40:
            self.direction*=-1
            self.movecounter*=-1
        
class Rope(pygame.sprite.Sprite):
    def __init__(self,x,y,movement):
        super().__init__()
        self.movement=movement
        self.image=pygame.image.load("images/rope.png")
        self.image=pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE*10))
        self.rect=self.image.get_rect(topleft=(x,y))
        self.mask=pygame.mask.from_surface(self.image)
        self.count=0
        self.direction=1
        self.velx=2

    def update(self):
        if self.movement:
            self.rect.x+=self.direction*self.velx
            self.count+=1
            if abs(self.count)>40:
                self.count*=-1
                self.direction*=-1

class Rock():
    def __init__(self,x,y):
         
        self.image=pygame.image.load("images/rock.png")
        self.x=x
        self.y=y
        self.random=random.randint(1,2)
        
        if self.random==1:
            self.image=pygame.transform.scale(self.image,(TILE_SIZE*2,TILE_SIZE))
        if self.random==2:
            self.image=pygame.transform.scale(self.image,(TILE_SIZE*4,TILE_SIZE*2))

        self.rect=self.image.get_rect(center=(self.x,self.y))
        self.mask=pygame.mask.from_surface(self.image)
        self.speedy=random.randint(4,8)
    
    def update(self):
        self.rect.y+=self.speedy
        screen.blit(self.image,self.rect)

        for block in world.tile_list:
            if block[1].colliderect(self.rect):
                self.rect.y=-50
                self.rect.x=random.randint(200,1200)
        
class Health(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("images/potionRed.png")
        self.image=pygame.transform.scale(self.image,(TILE_SIZE*4,TILE_SIZE*4))
        self.rect=self.image.get_rect(topleft=(x,y))
        self.mask=pygame.mask.from_surface(self.image)
                    
swing=Swing(49,37)

rock1=Rock(300,-50)
rock2=Rock(500,-50)
rock3=Rock(800,-50)
rock4=Rock(1000,-50)
              
class Player:
    def __init__(self,x,y):
        self.image=pygame.image.load("images/player.png") 
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.vely=0
        self.dy=0
        self.health=100
        self.canjump=False
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        self.direction=0 
        self.up=False
    def update(self):
         
        dx=0
        dy=0
        #MOVEMENT
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            dx+=5
            self.direction=1
        if keys[pygame.K_LEFT]:
            dx-=5
            self.direction=-1
        if keys[pygame.K_UP] and self.canjump:
            self.vely=-14.5
            self.canjump=False
        
      
        self.vely+=1
        if self.vely>12:
            self.vely=12
        dy+=self.vely
         
        #COLLISION WİTH WALL GROUND 
        for block in world.tile_list:
            if block[1].colliderect(self.rect.x, self.rect.y+dy , self.width, self.height):
                self.canjump=True
                if self.vely < 0:
                    dy = 0
                    self.vely = 0
                elif self.vely >= 0:
                    dy = 0
                    self.vely = 0

        for block in world.tile_list:
            if block[1].colliderect(self.rect.x+dx, self.rect.y , self.width, self.height):
                dx=0
        #COLLISON WİTH LAVA
        if pygame.sprite.spritecollide(self,lava_group,False,pygame.sprite.collide_mask):
            self.health-=100
             
        
        # COLLLISION WITH CACTUS
        if pygame.sprite.spritecollide(self,cactus_group,False,pygame.sprite.collide_mask):
            if self.direction==-1:
                self.rect.x+=20
            
            if self.direction==1:
                self.rect.x-=20
                
            self.health-=10
             
        
        
        # COLLISON WITH HEALTH BAR
        if pygame.sprite.spritecollide(self,health_group,True,pygame.sprite.collide_mask):
            self.health+=30
        
        #COLLISON WITH PIPE
        if pygame.sprite.spritecollide(self,pipe_group,False,pygame.sprite.collide_mask):
            self.canjump=False
            self.rect.x=1200        
            self.rect.y=330

        
        #COLLISON WITH PLATFORM
        if pygame.sprite.spritecollide(self,platform_group,False,pygame.sprite.collide_mask):
            dy=0
            self.vely=-1
             
            self.canjump=True
            
            if keys[pygame.K_SPACE] and self.canjump:
                self.vely=-14.5
                self.canjump=False
            dy+=self.vely
        
        #COLIISON WITH BALL
        if pygame.sprite.spritecollide(self,ball_group,False,pygame.sprite.collide_mask):
            self.health-=10
            if self.direction==-1:
                self.rect.x+=20
                dy+=10
            if self.direction==1:
                self.rect.x-=20
                dy+=10
        
        #COLLISION WITH ROPE 
         
        if pygame.sprite.spritecollide(self,rope_group2,False):
            self.rect.x=40
            self.up=True
             
        if self.up:
             
            self.vely=-1
            dy+=self.vely
            player.rect.y+=dy
             
            if self.rect.y<200:
                self.rect.x=60
                self.rect.y=230
                self.canjump=True
                self.up=False
        
        #COLLISION WITH ROCK
        if self.rect.colliderect(rock1.rect):
            rock1.rect.y=-50
            self.health-=25
        if self.rect.colliderect(rock2.rect):
            rock2.rect.y=-50
            self.health-=25
        if self.rect.colliderect(rock3.rect):
            rock3.rect.y=-50
            self.health-=25
        if self.rect.colliderect(rock4.rect):
            rock4.rect.y=-50
            self.health-=25
             

        self.rect.x+=dx
        self.rect.y+=dy  
        screen.blit(self.image,self.rect)

world=World(data)
player=Player(100,600)
 

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.exit()
    
     
    screen.blit(bgimage,(0,-200))
    text = font.render(f'Health --> {player.health}', True,(0,255,0))
    screen.blit(text, (30,30))
    
    world.draw()

    swing.update()
    
    # ROCKS
    if player.rect.y<300:
        rock1.update()
        rock2.update()
        rock3.update()
        rock4.update()
    

    lava_group.draw(screen)
    water_group.draw(screen)
    cactus_group.draw(screen) 
    platform_group.draw(screen)
    health_group.draw(screen)
    ball_group.draw(screen)
    rope_group.draw(screen)
    rope_group.update()
    rope_group2.draw(screen)
    rope_group2.update()
    pipe_group.draw(screen)
    platform_group.update()
    ball_group.update()
    player.update()

    if player.health<=0:
        player.canjump=False
        player.rect.x=100
        player.rect.y=600
        player.health=100
    
    if player.rect.x>1280:
        print("game over ")
        break

    pygame.display.flip()
    clock.tick(60)

