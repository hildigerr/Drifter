#!/usr/bin/python

import random

################################################################################
#                                                                              #
# Planets.py -- Planets and Solar Systems                                      #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

##################################################################### Constants:
DEFAULT_CIV_CHANCE = 50
MAX_BASE_CHANCE = 66
MIN_HEALTH = 25

civOpt = { 0:"Friendly", 1:"Neutral", 2:"Hostile" } # or None
civOptIdxMax = 2

##             I:( "Name", { N:("Resource", PRICE),... } QT )
planetType = { 0:( "Rock", { 0:("Dirt",       10 ),
                             1:("Stones",      5 ),
                             2:("Rocks",       8 ),
                             3:("Metal",      20 ),
                             4:("Gems",       50 )     }, 4 ),
               1:( "Watr", { 0:("Water",      12 ), 
                             1:("Ice",        18 ),
                             2:("Holy Water", 20 )     }, 2 ),
               2:( "Fire", { 0:("Charcoal",   11 ),
                             1:("Lava",       18 ),
                             2:("Obsidian",   20 ),
                             3:("Gems",       80 )     }, 3 ) }
planetTypeQt = 2


################################################################## Planet Class:
class Planet():
    '''
    type        -- Type of resources available on this planet.
                        ( "Name", {...,N:("Resource",worth)}, N )
    civ         -- Attitude of a planets citizens, if any.
    health      -- Remaining population, or resources, if any.
    baseChance  -- Base chance for gathering, fighting, etc.
    '''
    def __init__(self,civ_chance = DEFAULT_CIV_CHANCE):
        self.type = planetType[random.randint(0,planetTypeQt)]
        if random.randint(1,100) in range (1, civ_chance):
              self.civ = civOpt[random.randint(0,civOptIdxMax)]
              #TODO: Random Price Adjustments:
              #self.price = [] ; (n,res,qt) = self.type
              #for i in range (1,qt+1): self.price.append(random.randint(-5,5))
        else: self.civ = None
        self.health = random.randint(MIN_HEALTH,100)
        self.baseChance = random.randint(0,MAX_BASE_CHANCE)
        
    def harvest(self,adj = 0, bonus = 0):
        if self.health <= 0: return None
        result = adj + random.randint(1,100)
        if result > self.baseChance:
            (name,opt,qt) = self.type
            return opt[random.randint(0,qt)]
            
    #def buy(self,resource):
    #def sell(self,resource):
    #def trade(self,want,have):
    

        
################################################################## System Class:
class System():
    def __init__(self,maxQt,civ_chance = DEFAULT_CIV_CHANCE):
        self.qt = random.randint(0,maxQt)
        self.planets = []
        for i in range (1, self.qt): self.planets.append(Planet(civ_chance))
        self.pos = None
    def orbit(self,idx):
        if(( idx > 0 )and( idx < self.qt )): self.pos = idx
    def harvest(self):
        #TODO: Pass through any Modifiers
        if self.pos != None: self.planets[self.pos].harvest()


############################################################## Main for Testing:
if __name__ == '__main__':
    max_planets = 6
    sys = System(max_planets)
    
