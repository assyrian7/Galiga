'''
Created on Dec 28, 2014

@author: Paul
'''
import pygame
import random
import time
pygame.init()
pygame.mixer.init()
white = (255, 255, 255)
red =   (255, 0, 0)
green = (0, 255, 0)
blue =  (0, 0, 255)
black = (0, 0, 0)
width = 800
height = 600
screen = pygame.display.set_mode([width, height])
background = pygame.Surface(screen.get_size())
pygame.display.set_caption("Galiga 2.5")
laserblast = pygame.mixer.Sound("Audio\\Star Wars Blaster Sound Effect.ogg")
block_size = 30
font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((block_size, block_size))
        self.image.fill(blue)
        self.lasertimer = 0
        self.lasermax = 12
        self.damageTimer = 0
        self.damageMax = 100
        self.lives = 3
        self.damaged = False
        self.image = pygame.image.load("Textures\\Galiga.gif")      
        self.rect = self.image.get_rect()
        self.rect.center = (440, 400)
        
    def update(self):
        self.rect.x += self.change_x

        self.rect.y += self.change_y
        self.checkKeys()
        if (self.rect.right > screen.get_width()):
            self.rect.right = screen.get_width()
        elif (self.rect.left < 0):
            self.rect.left = 0
        elif (self.rect.bottom > screen.get_height()):
            self.rect.bottom = screen.get_height()
        elif (self.rect.top < 0):
            self.rect.top = 0
        if pygame.sprite.groupcollide(enemySprites, playerSprites, 1, 0) and self.damaged == False:
            self.lives -= 1
            score.lives -= 1
            self.damaged = True
            enemySprites.add(EnemyShip(random.randint(0, screen.get_width())))
        elif pygame.sprite.groupcollide(enemyLasers, playerSprites, 1, 0) and self.damaged == False:
            self.lives -= 1
            score.lives -= 1
            self.damaged = True
            enemySprites.add(EnemyShip(random.randint(0, screen.get_width())))
           
        if self.damaged == True:
            self.damageTimer += 1
            if self.damageTimer == self.damageMax:
                self.damaged = False
                self.damageTimer = 0
            
        if self.lives == 0 and score.lives == 0:
            gameOver = True                                              
    def checkKeys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.lasertimer += 1
            if self.lasertimer == self.lasermax:
                laserSprites.add(Laser(self.rect.center))
                self.lasertimer = 0
        if keys[pygame.K_LEFT]:
            self.goLeft()
            self.stopY()
        if keys[pygame.K_RIGHT]:
            self.goRight()
            self.stopY()
        if keys[pygame.K_UP]:
            self.goUp()
            self.stopX()
        if keys[pygame.K_DOWN]:
            self.goDown()
            self.stopX()

    def goLeft(self):
        self.change_x = -10
        self.change_y = 0
    def goRight(self):
        self.change_x = 10
        self.change_y = 0
    def goUp(self):
        self.change_y = -10
        self.change_x = 0
    def goDown(self):
        self.change_y = 10
        self.change_x = 0
    def stopX(self):
        self.change_x = 0
    def stopY(self):
        self.change_y = 0
class PlayerDamaged(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Textures\\Galiga_damaged.gif")
        self.rect = self.image.get_rect()
        self.counter = 0
        self.max = 100
        self.player = player
        self.damaged = False
        self.rect.center = [-100, -100]
        
    def update(self):
        if pygame.sprite.groupcollide(enemyLasers, playerSprites, 1, 0) and self.damaged == False:
            self.damaged = True
        elif pygame.sprite.groupcollide(enemySprites, playerSprites, 1, 0) and self.damaged == False:
            self.damaged = True
        if self.damaged == True:
            self.reset()
            self.counter += 1
            
            if self.counter == self.max:
                self.counter = 0
                self.damaged = False
                self.rect.center = [-100, -100]
    
    def reset(self):
        self.rect.center = self.player.rect.center

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((block_size / 3, block_size / 3))
        self.image.fill(red)
        self.pos = pos
        self.image = pygame.image.load("Textures\\Lazer1.gif")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.dy = -12
    def update(self):
        self.movement()
        if self.rect.top < 0:
            self.kill()
    def movement(self):
        self.rect.y += self.dy
class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((block_size / 3, block_size / 3))
        self.image.fill(red)
        self.pos = pos
        self.image = pygame.image.load("Textures\\Lazer1.gif")
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.dy = 12
    def update(self):
        self.movement()
        if self.rect.top > screen.get_height():
            self.kill()
            
    def movement(self):
        self.rect.y += self.dy
   
    
class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, centerx):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((block_size, block_size))
        self.image.fill(green)
        self.image = pygame.image.load("Textures\\Enemy1.gif")
        self.rect = self.image.get_rect()
        self.center = random.randint(0, screen.get_width())

        self.dy = 5
        
        self.reset()
    def update(self):
        self.movement()
        if self.rect.y > screen.get_height():
            self.reset()
        fire = random.randint(1, 60)
        if fire == 1:
            enemyLasers.add(EnemyLaser(self.rect.midbottom))
            fire = random.randint(1, 60)

        if pygame.sprite.groupcollide(enemySprites, laserSprites, 1, 1):
            score.score += 10
            enemyExplosions.add(EnemyExplosion(self.rect.center))
            center = random.randint(0, screen.get_width() / 2)
            enemySprites.add(EnemyShip(center))

           
        '''
        if pygame.sprite.groupcollide(enemySprites, playerSprites, 1, 1):
            score.lives -= 1
        '''
    def movement(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        
    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(5, 10)
        self.dx = random.randrange(-2, 2)
class EnemyScorpions(pygame.sprite.Sprite):
    def __init__(self, centerx):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Textures\\Enemy2.gif")
        self.rect = self.image.get_rect()
        center = random.randint(0, screen.get_width())
        self.spawnTimer = 0
        self.spawnMax = 100
                
        self.reset()
    def update(self):
        center = random.randint(0, screen.get_width())

        self.movement()
        if self.rect.y > screen.get_height():
            self.reset()
        if pygame.sprite.groupcollide(laserSprites, enemyScorpions, 1, 1):
            score.score += 10
        self.spawnTimer += 1
        '''
        if self.spawnTimer == self.spawnMax:
            enemyScorpions.add(EnemyScorpions(center))
            self.spawnTimer = 0
        '''
    def movement(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(5, 10)
        self.dx = random.randrange(-2, 2)

class EnemyExplosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((block_size, block_size))
        #self.image.fill(red)
        self.image = pygame.image.load("Textures\\explosion.gif")
        self.rect = self.image.get_rect()
        self.rect.center = pos        
        self.counter = 0
        self.maxcount = 10
    def update(self):
        self.counter = self.counter + 1
        if self.counter == self.maxcount:
            self.kill()
        
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((block_size * 3, block_size))
        self.image.fill(black)
        self.image = pygame.image.load("Textures\\boss.gif")
        self.rect = self.image.get_rect()
        self.dx = 8
        self.dy = 0
        self.lives = 30
        self.reset()
    def update(self):
        self.movement()
        if self.rect.right > screen.get_width() or self.rect.left < 0:
            self.dx *= -1
        fire = random.randint(0,9)
        if fire == 1:
            enemyLasers.add(EnemyLaser(self.rect.midbottom))
        if score.score == 1000:
            self.rect.centery = 50 
        if pygame.sprite.groupcollide(bossSprites, laserSprites, 0, 1):
            self.lives -= 1
            score.bossLives -= 1
    def movement(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
    def reset(self):
        self.rect.centerx = screen.get_width() / 2
        self.rect.centery = 700
class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 3
        self.score = 0
        self.bossLives = 2
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        self.text = "Lives: %d, Score: %d" %(self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 0, 0))
        self.rect = self.image.get_rect()
        
        
class Space(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Textures\\tarantula-nebula_01_800x600.jpg")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()   
def messageToScreen(msg, color):
    length = len(msg)
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, [250, screen.get_height() / 2])
def main():
    global gameWin
    gameExit = False
    gameOver = False
    gameWin = False
    global player 
    player = Player()
    global boss
    boss = Boss()
    global score 
    score = Scoreboard()
    global space
    space = Space()
    global playerDamaged
    playerDamaged = PlayerDamaged(player)
    screen.blit(background, (0, 0))
    allSprites = pygame.sprite.Group(space, score)
    global laserSprites
    laserSprites = pygame.sprite.Group()
    global enemySprites
    enemySprites = pygame.sprite.Group()
    enemySprites.add(EnemyShip(200))
    enemySprites.add(EnemyShip(300))
    enemySprites.add(EnemyShip(400))
    global enemyScorpions
    enemyScorpions = pygame.sprite.Group()
    enemyScorpions.add(EnemyScorpions(250))
    global enemyLasers
    enemyLasers = pygame.sprite.Group()
    global playerSprites
    playerSprites = pygame.sprite.Group(player)
    global playerDamageSprites
    playerDamageSprites = pygame.sprite.Group(playerDamaged)
    global bossSprites
    bossSprites = pygame.sprite.Group()
    bossSprites.add(boss)
    global enemyExplosions
    enemyExplosions = pygame.sprite.Group()
    while not gameExit:
        
        while gameOver == True:
            messageToScreen("Game Over! Press P to play again or Q to quit", red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        main()
                    elif event.key == pygame.K_q:
                        gameOver = False
                        gameExit = True
        while gameWin == True:
            messageToScreen("You won! Press P to play again or Q to quit", red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        main()
                    elif event.key == pygame.K_q:
                        gameWin = False
                        gameExit = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    laserblast.play()
                    
                
                elif event.key == pygame.K_ESCAPE:
                    gameExit = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.stopX()
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.stopY()
                
        if score.lives == 0:
            gameOver = True   
        elif score.bossLives == 0:
            gameWin = True
        
        
        clock.tick(60)
        #allSprites.clear(screen, background)
        #laserSprites.clear(screen, background)
        #enemySprites.clear(screen, background)
        #enemyLasers.clear(screen, background)
        #playerSprites.clear(screen, background)
        #bossSprites.clear(screen, background)
        allSprites.update()
        laserSprites.update()
        enemySprites.update()
        enemyLasers.update()
        bossSprites.update()
        enemyExplosions.update()
        enemyScorpions.update()
        playerSprites.update()
        playerDamageSprites.update()
        allSprites.draw(screen)
        laserSprites.draw(screen)
        enemySprites.draw(screen)
        enemyLasers.draw(screen)
        playerSprites.draw(screen)
        bossSprites.draw(screen)
        enemyExplosions.draw(screen)
        enemyScorpions.draw(screen)
        playerDamageSprites.draw(screen)
        pygame.display.flip()
    pygame.display.update()
    pygame.quit()
    quit()
if __name__ == "__main__":
    main()
