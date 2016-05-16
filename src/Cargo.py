#!/usr/bin/python

import random

################################################################################
#                                                                              #
# Cargo.py -- Resources, Modules, Comodities, etc.                             #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

##################################################################### Constants:
DEFAULT_CIV_CHANCE = 50

## Types ##
planetTypeQt = 3
planetType = { 0:"Barren", 1:"Rocky", 2:"Water", 3:"Fire" }

## Planet ##
# _RESOURCE_LIST = []
# _CHANCES = (harvest_chance_poor, harvest_chance_avg,
#             harvest_poor_min, harvest_poor_max,
#             harvest_avg_min,  harvest_avg_max,
#             harvest_good_min, harvest_good_max)
DEFAULT_CHANCES = (25, 90, 1, 20, 10, 33, 10, 25)
''' 25% chance only getting (1-20) of least valuable resouce.
    90% chance getting (10-33) of a random resource.
    10% chance getting (10-25) of most valuable resource. '''

## Barren Planet ##
BARREN_RESOUCE_LIST = ["Nothing","Dirt"]
BARREN_CHANCES = (50, 100, 0, 0, 0, 15, 0, 15 ) #50% chance of finding up to 15u dirt.

## Rocky Planet ##
ROCKY_RESOUCE_LIST = ["Dirt","Rocks","Stones","Metal","Gems"]
ROCKY_CHANCES = DEFAULT_CHANCES #TODO

## Water Planet ##
WATER_RESOUCE_LIST = ["Water","Ice","Holy Water"]
WATER_CHANCES = DEFAULT_CHANCES #TODO

## Fire Planet ##
FIRE_RESOUCE_LIST = ["Charcoal","Lava","Obsidian","Gems"]
FIRE_CHANCES = DEFAULT_CHANCES  #TODO

## Civilized Planet ##
ATTITUDE_RAND_MIN = 1
ATTITUDE_RAND_MAX = 100
ATTITUDE_FRIEND_MIN_DEFAULT = 50
ATTITUDE_ENEMY_MAX_DEFAULT = 25
CIV_HARVEST_ANGER_RAND_MAX = 15
CIV_DAM_MIN = 10
CIV_DAM_MAX = 33

################################################################## Civilization:
class Civilization():
    '''
    attitude   -- The civilizations attitude toward player as a percentage.
    fiendlyMin -- Minimum attitude for civilization to remain friendly.
    enemyMax   -- Civilization will be hostile until attitude reaches this max.
    '''
    def __init__(self,type,fri=ATTITUDE_FRIEND_MIN_DEFAULT,foe=ATTITUDE_ENEMY_MAX_DEFAULT):
        self.fiendlyMin = fri ; self.enemyMax = foe
        self.attitude = random.randint(ATTITUDE_RAND_MIN,ATTITUDE_RAND_MAX)
        #TODO: Random Price Adjustments:
        #self.price = [] ; (n,res,qt) = self.type
        #for i in range (1,qt+1): self.price.append(random.randint(-5,5))
    def Attitude(self,op=0):
        ''' Returns attitude string, and/or optionally modifies attitude.'''
        self.attitude += op
        if   self.attitude >= self.fiendlyMin:  return "Friendly"
        elif self.attitude >= self.enemyMax:    return "Neutral"
        else:                                   return "Hostile"

##################################################################### Resources:
resourceType = {    0:BARREN_RESOUCE_LIST,
                    1:ROCKY_RESOUCE_LIST,
                    2:WATER_RESOUCE_LIST,
                    3:FIRE_RESOUCE_LIST     }
resouceChances = {  0:BARREN_CHANCES,
                    1:ROCKY_CHANCES,
                    2:WATER_CHANCES,
                    3:FIRE_CHANCES     }
class Resource():
    '''
    type    -- Type of resources available on this planet.
    res     -- List of natural resources available on this planet.
    civ     -- The planet's civilization, if any.
    Private:
        harvest_chance_poor -- Chance of getting only poorest quality item.
        harvest_chance_avg  -- Chance of getting random item.
        harvest_poor_min    -- Minimum quantity recieved from poor harvest.
        harvest_poor_max    -- Maximum quantity recieved from poor harvest.
        harvest_avg_min     -- Minimum quantity recieved from random harvest.
        harvest_avg_max     -- Maximum quantity recieved from random harvest.
        harvest_good_min    -- Minimum quantity recieved from good harvest.
        harvest_good_max    -- Maximum quantity recieved from good harvest.
    '''
    def __init__(self,civ_chance=DEFAULT_CIV_CHANCE):
        r = random.randint(0,planetTypeQt)
        self.res  = resourceType[r] ; self.type = planetType[r]
        if random.randint(1,100) in range (1, civ_chance):
                self.civ = Civilization(r)
        else:   self.civ = None
        (self.harvest_chance_poor,self.harvest_chance_avg,
         self.harvest_poor_min,self.harvest_poor_max,
         self.harvest_avg_min,self.harvest_avg_max,
         self.harvest_good_min,self.harvest_good_max) = resouceChances[r]
    def harvest(self,bonus=0):
        '''Returns {'resource':quantity}. Assumes planet has verified success.'''
        result = {}
        if self.civ != None:
            if self.civ.Attitude(-random.randint(0,CIV_HARVEST_ANGER_RAND_MAX)) == "Hostile":
                result['Damage'] = random.randint(CIV_DAM_MIN,CIV_DAM_MAX) #TODO: apply modifiers
        chance = random.randint(0,100) #TODO: Get More Resources at a time?
        if chance <= self.harvest_chance_poor:
            result[min(self.res)] = random.randint(self.harvest_poor_min,self.harvest_poor_max) + bonus
        elif chance <= self.harvest_chance_avg:
            result[self.res[random.randint(0,len(self.res)-1)]] = random.randint(self.harvest_avg_min,self.harvest_avg_max) + bonus
        else: result[max(self.res)] = random.randint(self.harvest_good_min,self.harvest_good_max) + bonus
        return result
