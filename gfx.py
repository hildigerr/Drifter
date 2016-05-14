#!/usr/bin/python

################################################################################
#                                                                              #
# gfx.py -- Graphics Functions                                                 #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

import os, sys, time, pygame

from main import makeMilFalcon as Ship
# node.fuel = 100
# node.health = 100
# node.resources = {}
# node.damageMin = 8
# node.damageMax = 11
# node.currPlanet = None
from main import makePlanet as Planet
# node.planetNum = -1
# node.planetType = None
# node.resources = {}
# node.adjPlanets = []
# node.civ = None
# node.civHealth = None
# node.civStatus = None

##################################################################### Constants:
SCREEN_SIZE = (WIDTH_FULL, HEIGHT_FULL) = (800,600)

############################################################## Helper Functions:
def load_img(name):
    '''
    Function: load_img
    Parameter:
        name: The name of the image to load.
     The image is expected to be in the ./img directory
    '''
    name = os.path.join("img",name)
    try:
        img = pygame.image.load(name)
        if img.get_alpha() is None: img = img.convert()
        else: img = img.convert_alpha()
    except pygame.error, message:
        print "ERROR: Unable to load image:", name
        raise SystemExit, message
    return img, img.get_rect()

def save_img(me,name):
    '''
    Function: save_img
    Parameters:
        me: The image to be saved.
        name: The name of the directory to save the image in.
     The image will be saved as dat/name/timestamp.png
    '''
    name = os.path.join("dat",name)
    if not os.path.exists(name): os.makedirs(name)
    name = os.path.join(name,time.asctime())
    pygame.image.save(me,name+".png")

################################################################# Main Function:
def scene_gen(game,ship,planet):
    '''
    Function: scene_gen -- Generate's Scene Image
    Parameters:
        game: Name of current game. Used to organize saved images.
        ship: The Ship.
        planet: The Ship's currPlanet.
    '''
    screen = pygame.display.set_mode(SCREEN_SIZE)
    (splash,s_rect) = load_img("star-field.png")
    screen.blit(splash,s_rect)

#     if pygame.font:
#         font = pygame.font.Font(None, 32)
#         font.set_bold(True)
#     else:
#         print "ERROR: Pygame: Unable to load font."
#         pygame.quit()
#         sys.exit(1)
    
    # pygame.display.flip()
    save_img(screen,game)

############################################################## Main for Testing:
if __name__ == '__main__':
    from main import genPlanetResources
    craft = Ship()
    planet = Planet()
    res = genPlanetResources(planet)
    scene_gen("Testing",craft,planet)
    # while( True ): print "testing"
