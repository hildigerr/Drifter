#!/usr/bin/python

################################################################################
#                                                                              #
# Graphics.py -- Graphics Functions                                            #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

import os, sys, time, math, pygame

import Ship

from Cargo import planetType

##################################################################### Constants:
RAD = 0.0174533 # One Degree Radian

## Tuning Parameters ##
SCREEN_SIZE = (WIDTH_FULL, HEIGHT_FULL) = (800,600)

## Round Dashboard ##
DASH_IMG_NAME = "dash-round.png"
FUEL_GUAGE_START_LOC = (140,570)
FUEL_GUAGE_OFFSET    = 15.0
FUEL_GUAGE_LINE_LEN  = 60
FUEL_GUAGE_LINE_WID  = 2
DASH_DELTA_TOP_RIGHT  = (466,362) # TOP_LEFT-->(351,362)


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
    except (pygame.error, message):
        print ("ERROR: Unable to load image:", name)
        raise (SystemExit, message)
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
def scene_gen(game,player,screen):
    '''
    Function: scene_gen -- Generate's Scene Image
    Parameters:
        game: Name of current game. Used to organize saved images.
        player: The Ship.
        screen: The Screen Display.
    '''
    # Draw Background #
    (splash,s_rect) = load_img("star-field.png")
    screen.blit(splash,s_rect)
    
    # Draw the Dashboard #
    (splash,s_rect) = load_img(DASH_IMG_NAME)
    screen.blit(splash,s_rect)
    
    # Draw Fuel Gauge Indicator #
    pygame.draw.line(screen, pygame.Color("red"), 
        FUEL_GUAGE_START_LOC, get_fuel_line_end(player.fuel), FUEL_GUAGE_LINE_WID)
    
    
    ## Render Textual Output ##
    pygame.font.init()
    if pygame.font:
        font = pygame.font.SysFont("monospace",15)
        font.set_bold(True)
    else:
        print ("ERROR: Pygame: Unable to load font.")
        pygame.quit()
        sys.exit(1)
    
    # Display Distance From Home #
    textBox = font.render(str(player.delta),1,pygame.Color("green"))
    t_rect = textBox.get_rect()
    t_rect.topright = DASH_DELTA_TOP_RIGHT
    screen.blit(textBox,t_rect)
    
    # Draw Current Planet #
    if player.sys.pos != None:
        planet = player.sys.planets[player.sys.pos]
        kind   = planet.resource.type
        if   kind == "Rocky": (splash,s_rect) = load_img("planet000.png")
        elif kind == "Water": (splash,s_rect) = load_img("planet001.png")
        elif kind == "Fire":  (splash,s_rect) = load_img("planet002.png")
        else:                 (splash,s_rect) = load_img("planet003.png")# "Barren"
        s_rect.center = (0,0)
        screen.blit(splash,s_rect)
        if planet.resource.civ != None:
            (splash,s_rect) = load_img("city-overlay.png")
            s_rect.center = (0,0)
            screen.blit(splash,s_rect)

    #save_img(screen,game)#TODO Do save the img when testing is done!
    return screen

############################################################## Main for Testing:
if __name__ == '__main__':
    scene_gen( "Testing", Ship.Ship(), pygame.display.set_mode(SCREEN_SIZE) )    
    # pygame.display.flip()
    pygame.quit()
