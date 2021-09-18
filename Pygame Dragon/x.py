import pygame, os, random, time
from pygame.locals import *

# set up the window
WINDOWWIDTH = 256
WINDOWHEIGHT = 232

def load_image(filename):
    image = pygame.image.load(filename)
    #image = image.convert()            #faster
    image = image.convert_alpha()       #slower, but works w/ transparent
    return image

def display_title1(windowSurface, image, duration):
    starttime = time.time()
    runtime = 0
    windowSurface.blit(image, (0,0))
    pygame.display.update()
    pygame.event.pump()
    pygame.time.delay(5000)

    
def display_title(windowSurface, image, duration):
    starttime = time.time()
    runtime = 0
    windowSurface.blit(image, (0,0))
    pygame.display.update()
    while runtime < duration:
        print(runtime)
        runtime = time.time() - starttime
        


def main():   
    # set up pygame
    pygame.init()
    mainClock = pygame.time.Clock()

    #Set up the windowSurface
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('DOUBLE DRAGON')

    titleimg = load_image("title.png")
    display_title1(windowSurface, titleimg, 5000)
    pygame.quit()
    os._exit(1)


main()
