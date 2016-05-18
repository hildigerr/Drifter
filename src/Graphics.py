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
FUEL_GUAGE_OFFSET    =  15.0
FUEL_GUAGE_LINE_LEN  =  60
FUEL_GUAGE_LINE_WID  =  2
DASH_DELTA_TOP_RIGHT = (466,362) # TOP_LEFT-->(351,362)
SHIELD_STATUS_CENTER = (575,435)

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
        #TODO: NameError: global name 'message' is not defined
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

##################################################################### PlanetSys:
#TODO
class PlanetSys():
    #TODO: Have muliple planet images of each kind and randomize selection.
    #TODO: Rotate the spheres randomly to simulate time passing in orbit.
    def __init__(self):
        self.planetImg = {}
        self.planetImg["Rocky" ] = load_img("planet000.png")
        self.planetImg["Water" ] = load_img("planet001.png")
        self.planetImg["Fire"  ] = load_img("planet002.png")
        self.planetImg["Barren"] = load_img("planet003.png")
        self.stockSolarSystemImg = load_img("star-chart-6.png" )
        self.solarSystemImg = None
    def gen_sys(self):
        pass #TODO

############################################################### ShieldIndicator:
class ShieldIndicator():
    def __init__(self):                                 #  STATUS  # 
        self.images = [load_img("shield-red.png"),      #  0 - 29  #
                       load_img("shield-orange.png"),   # 30 - 49  #
                       load_img("shield-yellow.png"),   # 50 - 69  #
                       load_img("shield-green.png"),    # 70 - 89  #
                       load_img("shield-blue.png")]     # 90 - 100 #
    def get(self,status):
        if status < 30: return self.images[0]           # RED      #
        if status < 50: return self.images[1]           # ORANGE   #
        if status < 70: return self.images[2]           # YELLOW   #
        if status < 90: return self.images[3]           # GREEN    #
        else:           return self.images[4]           # BLUE     #

################################################################ Graphics Class:
class Graphics():
    '''
    name:   Name of current game. Used to organize saved images.
    player: The Ship.
    '''
    def __init__(self,name,player):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.name = name ; self.player = player
        self.sh = ShieldIndicator()
        self.sys = PlanetSys()
        pygame.font.init()
        if pygame.font:
            self.font = pygame.font.SysFont("monospace",15)
            self.font.set_bold(True)
        else:
            print ("ERROR: Pygame: Unable to load font.")
            pygame.quit()
            sys.exit(1)
        (self.bg,self.bg_rect) = load_img("star-field.png")
        (self.db,self.db_rect) = load_img(DASH_IMG_NAME)
    def scene_gen(self,sol_sys=None):
        '''Generate's Scene Image '''
        self.screen.blit(self.bg,self.bg_rect) # Draw Background    #
        self.screen.blit(self.db,self.db_rect) # Draw the Dashboard #
        
        # Draw Fuel Gauge Indicator #
        pygame.draw.line(self.screen, pygame.Color("red"), 
            FUEL_GUAGE_START_LOC, get_fuel_line_end(self.player.fuel), FUEL_GUAGE_LINE_WID)
    
        # Draw Shield Status Indicator #
        (splash, splash_rect) = self.sh.get(self.player.health)
        splash_rect.center = SHIELD_STATUS_CENTER
        self.screen.blit(splash,splash_rect)
        #TODO: Write str(self.player.health) over image.
    
        # Display Distance From Home #
        txt = self.font.render(str(self.player.delta),1,pygame.Color("green"))
        txt_rect = txt.get_rect()
        txt_rect.topright = DASH_DELTA_TOP_RIGHT
        self.screen.blit(txt,txt_rect)
    
        # Draw Current Planet #
        if self.player.sys.pos != None:
            planet = self.player.sys.planets[self.player.sys.pos]
            kind   = planet.resource.type
            (splash,s_rect) = self.sys.planetImg.get(kind,"Barren")
            s_rect.center = (0,0)
            self.screen.blit(splash,s_rect)
            if planet.resource.civ != None:
                (splash,s_rect) = load_img("city-overlay.png")
                s_rect.center = (0,0)
                self.screen.blit(splash,s_rect)

        #save_img(self.screen,self.name)#TODO Do save the img when testing is done!

############################################################## Main for Testing:
if __name__ == '__main__':
    scene_gen( "Testing", Ship.Ship(), pygame.display.set_mode(SCREEN_SIZE) )    
    # pygame.display.flip()
    pygame.quit()
