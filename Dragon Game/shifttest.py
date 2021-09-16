import pygame, os, random, time
from pygame.locals import *

# set up the window
WINDOWWIDTH = 256
WINDOWHEIGHT = 232

FRAMERATE = 40

def Terminate():
    pygame.quit()
    os._exit(1)

def process_events(x, windowSurface, move):
    """Respond to keyboard and mouse clicks"""
    for event in pygame.event.get():
        if event.type == QUIT:
            Terminate()
        elif event.type == KEYDOWN:
            # update the direction of the player
            if event.key == K_LEFT or event.key == ord('a'):
                move = [True, False]
            elif event.key == K_RIGHT or event.key == ord('d'):
                move = [False, True]
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == ord('a'):
                move = [False, False]
            elif event.key == K_RIGHT or event.key == ord('d'):
                move = [False, False]
            # player wants to quit
            if event.key == K_ESCAPE:
                Terminate()
    return move

def load_image(filename):
    image = pygame.image.load(filename)
    image = image.convert()             #faster
    #image = image.convert_alpha()      #slower, but works w/ transparent
    return image

def display_frame(self, windowSurface):
    """Update the screen"""

    

    # draw the window onto the screen
    pygame.display.update()
        
def main():   
    # set up pygame
    pygame.init()
    mainClock = pygame.time.Clock()

    #Set up the windowSurface
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('DOUBLE DRAGON')

    bg = load_image("background1.png")
    imgrect = bg.get_rect()
    width = -(imgrect.width - WINDOWWIDTH)
    print(width)
    x = 0
    move = [False, False]
    # run the game loop
    while True:
        
        move = process_events(x, windowSurface, move)
        if move[0] and x < 0:
            x += 1
        elif move[1] and x > (width):
            x -= 1
        windowSurface.blit(bg, (x, 0))

        pygame.display.update()

        # update the clock    
        mainClock.tick(FRAMERATE)

main()
