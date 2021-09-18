import pygame, os, random, time
from pygame.locals import *

# set up the window
WINDOWWIDTH = 256
WINDOWHEIGHT = 232

# set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 240, 0)

# set up the frame rate
FRAMERATE = 40

# set up move speed
MAINMOVESPEED = 3
OPPMOVESPEED = 1

# set up jumping
JUMPTIME = 5

# set up health
MAINHEALTH = 3
MAINLIVES = 3
OPPHEALTH = 3

def Terminate():
    pygame.quit()
    os._exit(1)

def drawText(message, font, windowSurface, x, y, textcolour):
    text = font.render(message, 1, textcolour)
    textrect = text.get_rect()
    textrect.topleft = (x, y)
    windowSurface.blit(text, textrect)

class Player(pygame.sprite.Sprite):
    def __init__(self, image, health, lives, movespeed, jumptime):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOWWIDTH//2
        self.rect.centery = WINDOWHEIGHT//2
        # initialize movement variables
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.lives = lives
        self.health = health
        self.score = 0
        self.movespeed = movespeed
        self.attack = False
        self.attackTime = 0
        self.jumping = False
        self.jumpCount = jumptime
        self.isHit = False
        self.isDead = False
        self.facingRight = False
        self.facingLeft = False

    def update(self, rightimg, leftimg, attackimgright, attackimgleft, jumptime):#, attackimg)
        # moving the player
        if self.moveDown and self.rect.bottom <= WINDOWHEIGHT - 40:
            self.rect.top += self.movespeed
        elif self.moveUp and self.rect.top >= 0:
            self.rect.top -= self.movespeed
        elif self.moveLeft and self.rect.left >= 10*self.movespeed:
            self.rect.left -= self.movespeed
            self.image = leftimg
            self.facingLeft = True
            self.facingRight = False
        elif self.moveRight and self.rect.right <= WINDOWWIDTH - 10*self.movespeed:
            self.rect.right += self.movespeed
            self.image = rightimg
            self.facingRight = True
            self.facingLeft = False

        # when player is attacking
        if self.attack:
            if self.facingRight:
                self.image = attackimgright
            if self.facingLeft:
                self.image = attackimgleft
            self.attack = False
        else:
            if time.time() - self.attackTime >= 0.5:
                if self.facingRight:
                    self.image = rightimg
                if self.facingLeft:
                    self.image = leftimg
        
        # for jumping
        if self.jumping:
            if self.jumpCount >= -5:
                time.sleep(0.03)
                self.rect.top -= self.jumpCount*abs(self.jumpCount)
                self.jumpCount -= 1
            else:
                self.jumpCount = jumptime
                self.jumping = False

        # when player is getting attacked
        if self.isHit:
            self.health -= 1
            self.isHit = False
            #self.image.fill((190, 0, 0, 100), special_flags=pygame.BLEND_ADD)
            #KFIAOFKAFKJAFHNAEFHNALJFKSL FUCK FUCKL FUCK FUCK 

        # check player's vitals
        if self.health <= 0 and not self.isDead:
            self.lives -= 1
            if self.lives <= 0:
                self.isDead = True
            else:
                self.health = MAINHEALTH

    # WHY DOES IT LAND HIGHER ------- need to use int values for rect.pos!
        
        # player action
        # elif self.attack:
            # self.image = attackimg
            
class Opps(pygame.sprite.Sprite):
    def __init__(self, image, health, movespeed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        # get random position
        self.rect.left = random.randrange(0, WINDOWWIDTH - self.rect.width)
        self.rect.top = random.randrange(0, WINDOWHEIGHT - self.rect.width)
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.attack = False
        self.stallAttack = False
        self.facingRight = False
        self.facingLeft = False
        self.isHit = False
        self.isDead = False
        self.attackTime = 0
        self.attackDuration = 0.3
        self.stallTime = 2
        self.health = health
        self.movespeed = movespeed

    def update(self, rightimg, leftimg, attackimgright, attackimgleft):
        #moving the opponents
    #GOING TO BE BASED ON MAINPLAYER'S POSITION
        if self.moveDown and self.rect.bottom <= WINDOWHEIGHT - 40:
            self.rect.top += self.movespeed
        elif self.moveUp and self.rect.top >= 0:
            self.rect.top -= self.movespeed
        elif self.moveLeft and self.rect.left >= 10*self.movespeed:
            self.rect.left -= self.movespeed
            self.image = leftimg
            self.facingLeft = True
            self.facingRight = False
        elif self.moveRight and self.rect.right <= WINDOWWIDTH - 10*self.movespeed:
            self.rect.right += self.movespeed
            self.image = rightimg
            self.facingRight = True
            self.facingLeft = False

        # when opponent is hit
        if self.isHit:
            self.health -= 1
            self.isHit = False

        # check opponent's vitals
        if self.health <= 0:
            self.isDead = True

        # initiating opponent attack
        if self.attack:
            if self.facingRight:
                self.image = attackimgright
            if self.facingLeft:
                self.image = attackimgleft
            self.attack = False
        else:
            if time.time() - self.attackTime >= 0.5:
                if self.facingRight:
                    self.image = rightimg
                if self.facingLeft:
                    self.image = leftimg

class Game():
    def __init__(self):
        
        self.game_over = False
        self.starttime = time.time()

        #set up sprites group for display
        self.all_sprites = pygame.sprite.Group()

        #set up player
        self.prightimg = load_image('walk_right.png')
        self.pleftimg = load_image('walk_left.png')
        self.pattackrightimg = load_image('attack_right.png')
        self.pattackleftimg = load_image('attack_left.png')
        self.player = Player(self.prightimg, MAINHEALTH, MAINLIVES, MAINMOVESPEED, JUMPTIME)
        #add to sprites group
        self.all_sprites.add(self.player)

        #set up opponents (group)
        self.opps = pygame.sprite.Group()
        self.orightimg = load_image('opp_right.png')
        self.oleftimg = load_image('opp_left.png')
        self.oattackrightimg = load_image('opp_attack_right.png')
        self.oattackleftimg = load_image('opp_attack_left.png')
        anopp = Opps(self.oleftimg, OPPHEALTH, OPPMOVESPEED)
        self.opps.add(anopp)
        self.all_sprites.add(anopp)
        ##OPPS TO SPAWN WHEN PLAYER REACHES A CERTAIN DISTANCE

        #set up background
        self.bgimg = load_image('background1.png')
        bgrect = self.bgimg.get_rect()
        self.bgwidth = -(bgrect.width - WINDOWWIDTH)
        self.bgpos = 0
        
        # set up music
        self.punchSound = pygame.mixer.Sound('PUNCH.wav')
        pygame.mixer.music.load('POL-last-samurai-short.wav')
        self.gameOverVoice = pygame.mixer.Sound('game_over_voice.wav')
        self.winnerVoice = pygame.mixer.Sound('winner_voice.mp3')
        self.loserSound = pygame.mixer.Sound('game_over_music.wav')
        self.winnerSound = pygame.mixer.Sound('stage_clear_music.wav')
        self.musicplaying = True

        # Play the background music
        pygame.mixer.music.play(-1, 0.0)
        self.musicPlaying = True
        
    def process_events(self, windowSurface):
        """Respond to keyboard and mouse clicks"""
        for event in pygame.event.get():
            if event.type == QUIT:
                Terminate()
            elif event.type == KEYDOWN:
                # update the direction of the player
                if event.key == K_LEFT or event.key == ord('a'):
                    self.player.moveLeft = True
                    self.player.moveRight = False
                elif event.key == K_RIGHT or event.key == ord('d'):
                    self.player.moveRight = True
                    self.player.moveLeft = False
                elif event.key == K_UP or event.key == ord('w'):
                    self.player.moveUp = True
                    self.player.moveDown=False
                elif event.key == K_DOWN or event.key == ord('s'):
                    self.player.moveDown = True
                    self.player.moveUp = False

                if event.key == K_SPACE:
                    self.player.jumping = True

                if event.key == ord('b'):
                    self.player.attack = True
                    self.player.attackTime = time.time()
                    
            elif event.type == KEYUP:
                # the player has stopped moving
                if event.key == K_LEFT or event.key == ord('a'):
                    self.player.moveLeft = False
                elif event.key == K_RIGHT or event.key == ord('d'):
                    self.player.moveRight = False
                elif event.key == K_UP or event.key == ord('w'):
                    self.player.moveUp = False
                elif event.key == K_DOWN or event.key == ord('s'):
                    self.player.moveDown = False

                # player wants to quit
                if event.key == K_ESCAPE:
                    Terminate()

                # the user wants to mute music
                elif event.key == ord('m'):
                    if self.musicplaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    self.musicplaying = not self.musicplaying
                
##            elif event.type == pygame.MOUSEBUTTONDOWN:
##                #The user clicks to restart the game when it is over
##                if self.game_over:
##                    #start new game
##                    display_settings(windowSurface)
##                    stats = run_settings()
##                    self.__init__(stats)

    def run_logic(self):
        """ Check for collisions"""
        # check if the player has attacked any opponents; vice versa
        # check where the opp needs to move to

        if len(self.opps) == 0 or self.player.isDead:
            self.game_over = True
            pygame.mixer.music.stop()
            #if self.musicplaying:
                #self.gameOverSound.play()
        
        for anopp in self.opps:

            if anopp.isDead:
                anopp.kill()

            attack_stall = time.time() - anopp.attackTime
            if attack_stall >= anopp.attackDuration:
                anopp.attack = False
            
            if anopp.rect.top > self.player.rect.top:
                anopp.moveUp = True
                anopp.moveDown = False
                attack_posx = False
            elif anopp.rect.bottom < self.player.rect.bottom:
                anopp.moveDown = True
                anopp.moveUp = False
                attack_posx = False
            else:
                anopp.moveUp = False
                anopp.moveDown = False
                attack_posx = True
                
            if anopp.rect.left > self.player.rect.left + 20:
                anopp.moveLeft = True
                anopp.moveRight = False
                attack_posy = False
            elif anopp.rect.right < self.player.rect.right - 20:
                anopp.moveRight = True
                anopp.moveLeft = False
                attack_posy = False
            else:
                anopp.moveLeft = False
                anopp.moveRight = False
                attack_posy = True

            if attack_posy and attack_posx:

                opp_stall = time.time() - anopp.attackTime
                if opp_stall >= anopp.stallTime:
                    anopp.attack = True
                    anopp.attackTime = time.time()
                    if self.player.jumping == False:
                        self.player.isHit = True
                        self.punchSound.play()

                if self.player.attack == True:
                    if self.player.facingRight and anopp.facingLeft or self.player.facingLeft and anopp.facingRight:
                        anopp.isHit = True
                        self.punchSound.play()
                        
            anopp.update(self.orightimg, self.oleftimg, self.oattackrightimg, self.oattackleftimg)

        self.player.update(self.prightimg, self.pleftimg, self.pattackrightimg, self.pattackleftimg, JUMPTIME) #, self.pattackimg)
            

    def display_frame(self, windowSurface, windowwidth):
        """Update the screen"""
        # draw the black background onto the surface
        #IMPLEMENT THE SCROLLING BACKGROUND
        #background should scroll when player is moving towards off-screen
        #when player.rect.right is at ~15 from maxwidth or at ~15 or something

        if self.player.rect.right >= windowwidth - 10*self.player.movespeed and self.player.moveRight:
            if self.bgpos > self.bgwidth:
                self.bgpos -= self.player.movespeed
        elif self.player.rect.left <= 10*self.player.movespeed and self.player.moveLeft:
            if self.bgpos < 0:
                self.bgpos += self.player.movespeed

        windowSurface.blit(self.bgimg,(self.bgpos,0))
        self.all_sprites.draw(windowSurface)

        # draw the window onto the screen

    def display_stats(self, windowSurface, lives, health, score, WINDOWWIDTH, WINDOWHEIGHT):
        message_lives = "LIVES: "+str(lives)
        message_health = "HEALTH: "+str(health)
        message_score = "SCORE: "+str(score)

        font = pygame.font.SysFont("applesgothicneo", 16)
        
        text_lives = font.render(message_lives, True, YELLOW)
        text_health = font.render(message_health, True, YELLOW)
        text_score = font.render(message_score, True, YELLOW)

        textRect_lives = text_lives.get_rect()
        textRect_health = text_health.get_rect()
        textRect_score = text_score.get_rect()

        textRect_lives.bottomleft = (WINDOWWIDTH - 45, WINDOWHEIGHT)
        textRect_health.bottomleft = (0,WINDOWHEIGHT - 12)
        textRect_score.bottomleft = (0,WINDOWHEIGHT)

        windowSurface.blit(text_lives, textRect_lives)
        windowSurface.blit(text_health, textRect_health)
        windowSurface.blit(text_score, textRect_score)

def load_image(filename):
    image = pygame.image.load(filename)
    #image = image.convert()            #faster
    image = image.convert_alpha()       #slower, but works w/ transparent
    return image

def display_title(windowSurface, image, duration):
    starttime = time.time()
    runtime = 0
    windowSurface.blit(image, (0,0))
    pygame.display.update()
    pygame.event.pump()
    pygame.time.delay(duration)
        
#def run_menu():
    ##need to create the images

def game_over(windowSurface, game):
        windowSurface.fill(BLACK)
        # The user will click to restart the game
        x = WINDOWWIDTH // 2 - 80
        y = WINDOWHEIGHT // 2 - 20
        font = pygame.font.SysFont('couriernewboldttf', 20)
        if game.player.lives == 0:
            game.gameOverVoice.play()
            drawText("GAME OVER! you lost, kid.", font, windowSurface, x, y, YELLOW)
        else:
            #game.winnerVoice.play()
            drawText("KO! WINNER!", font, windowSurface, x+25, y, YELLOW)
        pygame.display.update()
        
def main():   
    # set up pygame
    pygame.init()
    mainClock = pygame.time.Clock()

    #Set up the windowSurface
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('DOUBLE DRAGON')

    #Run Pre-Game Menu Page

    #set up game!
    game = Game()
  
    titleimg = load_image("title.png")
    display_title(windowSurface, titleimg, 3000)
    
    # run the game loop
    while True:
        game.process_events(windowSurface)
        
        if not game.game_over:
            #so that uneseccary functions dont run
            #and sounds don't play during gameover screen
            game.run_logic()
            game.display_frame(windowSurface, WINDOWWIDTH)
            game.display_stats(windowSurface, game.player.lives, game.player.health, game.player.score, WINDOWWIDTH, WINDOWHEIGHT)
            pygame.display.update()
        else:
            if game.player.lives == 0:
                game.loserSound.play()
            else:
                game.winnerSound.play()
            time.sleep(4)
            break
        # update the clock    
        mainClock.tick(FRAMERATE)  
        
    game_over(windowSurface, game)


main()

