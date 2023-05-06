from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,x,y,sizex,sizey,player_speed):
        super().__init__()
        self.image=transform.scale(image.load(player_image),(65,65))
        self.speed=player_speed

        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys= key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -=self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x +=self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        pgrops.add(bullet)
lost=0
class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global lost
        if self.rect.y>win_height:
            self.rect.x=randint(80,win_width-80)
            self.rect.y=0
            lost+=1

class Bullet (GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

pgrops = sprite.Group()

win_width=700
win_height=500
window=display.set_mode((win_width,win_height))
display.set_caption('Galaxy')

background=transform.scale(image.load("galaxy.jpg"),(win_width,win_height))
ship=Player('rocket.png',5,win_height - 100,80,100,10)
monsters=sprite.Group()
for i in range(1,6):
    vrag = Enemy('ufo.png',randint(80,win_width-80),-40,80,50,randint(1,1))
    monsters.add(vrag)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
clock=time.Clock()
game=True
finish=False
score=0
stop=3
goal=10
font.init()
font2=font.Font(None,36)
while game:
    for e in event.get():
        if e.type ==QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()

    if not finish:
        window.blit(background,(0,0))

        text = font2.render('Счёт:'+ str(score),1,(255,255,255))
        window.blit(text,(10,20))

        text_lise=font2.render('Пропущено:'+str(lost),1,(255,255,255))
        window.blit(text_lise,(10,50))
        
        pgrops.update()
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        pgrops.draw(window)

        collide=sprite.groupcollide(monsters, pgrops, True, True)
        for c in collide:
            score+=1
            vrag = Enemy('ufo.png',randint(80,win_width-80),-40,80,50,randint(1,5))
            vrag.add(monsters)
        if sprite.spritecollide(ship,monsters, False) or lost >= stop:
            finish=True
        if score >=goal:
            finish=True
    
    else:
       finish = False
       score = 0
       lost = 0
       for b in pgrops:
           b.kill()
       for m in monsters:
           m.kill()
       time.delay(3000)
       for i in range(1, 6):
           vrag = Enemy('ufo.png',randint(80,win_width-80),-40,80,50,randint(1,1))
           monsters.add(vrag)
    display.update()
    clock.tick(60)