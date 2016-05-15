#!/usr/bin/python

################################################################################
#                                                                              #
# gfx.py -- Graphics Functions                                                 #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

import os, sys, time, math, pygame

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
RAD = 0.0174533 # One Degree Radian

## Tuning Parameters ##
SCREEN_SIZE = (WIDTH_FULL, HEIGHT_FULL) = (800,600)

## Round Dashboard ##
DASH_IMG_NAME = "dash-round.png"
FUEL_GUAGE_START_LOC = (140,570)
FUEL_GUAGE_OFFSET = 15.0
FUEL_GUAGE_LINE_LEN = 60
FUEL_GUAGE_LINE_WID = 2

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
    
def get_fuel_line_end(qt):
    '''
    Function: get_fuel_line_end
    Parameter:
        qt: The quantity of fuel to gauge.
     Determines the endpoint of the fuel gauge indicator line.
     The angle is offset by n degrees radian, and scaled by the qt as a percentage.
    '''
    import operator as op
    n = FUEL_GUAGE_OFFSET * RAD
    omega = n + (qt/100.0)*(math.pi - (2*n))
    y =  FUEL_GUAGE_LINE_LEN * math.sin(-omega)
    x = -FUEL_GUAGE_LINE_LEN * math.cos(-omega)
    return tuple(map(op.add, FUEL_GUAGE_START_LOC, (x,y)))

################################################################# Main Function:
def scene_gen(game,ship,planet):
    '''
    Function: scene_gen -- Generate's Scene Image
    Parameters:
        game: Name of current game. Used to organize saved images.
        ship: The Ship.
        planet: The Ship's currPlanet.
    '''
    # Draw Background #
    screen = pygame.display.set_mode(SCREEN_SIZE)
    (splash,s_rect) = load_img("star-field.png")
    screen.blit(splash,s_rect)
    
    # Draw Fuel Gauge #
    (splash,s_rect) = load_img(DASH_IMG_NAME)
    screen.blit(splash,s_rect)
    pygame.draw.line(screen, pygame.Color("red"), 
        FUEL_GUAGE_START_LOC, get_fuel_line_end(ship.fuel), FUEL_GUAGE_LINE_WID)
        
    # Draw Current Planet #
    if ship.currPlanet != None:
        print "Testing: ", planet.planetType
        if   planet.planetType == "Rock": (splash,s_rect) = load_img("planet000.png")
        elif planet.planetType == "Watr": (splash,s_rect) = load_img("planet000.png")
        elif planet.planetType == "Fire": (splash,s_rect) = load_img("planet000.png")
        else:                             (splash,s_rect) = load_img("planet000.png")
        s_rect.center = (0,0)
        screen.blit(splash,s_rect)
        if planet.civ != None:
            (splash,s_rect) = load_img("city-overlay.png")
            s_rect.center = (0,0)
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
    craft.currPlanet = Planet()
    res = genPlanetResources(craft.currPlanet)
    scene_gen("Testing",craft,craft.currPlanet)
    # while( True ): print "testing"
