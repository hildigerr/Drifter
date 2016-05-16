#!/usr/bin/python
################################################################################
#                                                                              #
# Cargo.py -- Resources, Modules, Comodities, etc.                             #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

import random


##################################################################### Constants:
DEFAULT_CIV_SPAWN_CHANCE = 50

## Planet Types ##
planetTypeQt = 3
planetType = { 0:"Barren", 1:"Rocky", 2:"Water", 3:"Fire" }

## XXX Planet ##
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


resourceType = {    0:BARREN_RESOUCE_LIST,
                    1:ROCKY_RESOUCE_LIST,
                    2:WATER_RESOUCE_LIST,
                    3:FIRE_RESOUCE_LIST     }
resouceChances = {  0:BARREN_CHANCES,
                    1:ROCKY_CHANCES,
                    2:WATER_CHANCES,
                    3:FIRE_CHANCES     }

refineConversions = { "Rocks":"Stones","Stones":"Gems",
                      "Ice":"Water","Water":"Holy Water","Holy Water":"Fuel",
                      "Lava":"Obsidian","Obsidian":"Gems","Charcoal":"Fuel" }

## Civilized Planet ##
ATTITUDE_RAND_MIN =             1 # Minimum Initial Attitude                # 
ATTITUDE_RAND_MAX =           100 # Maximum Initial Attitude                # 
ATTITUDE_FRIEND_MIN_DEFAULT =  50 # Defaulf Min Attitude to be Friendly     # 
ATTITUDE_ENEMY_MAX_DEFAULT =   25 # Default Max Attitude to be Hostile      # 
ATTITUDE_PRICE_ADJ_MIN =        1 # Minimum price adjustment from Attitude  # 
ATTITUDE_PRICE_ADJ_MAX =       10 # Maximum price adjustment from Attitude  # 
RND_PRICE_ADJ_MIN =           -10 # Minimum Random price adjustment         # 
RND_PRICE_ADJ_MAX =            10 # Maximum Random price adjustment         # 
PRICE_LOCAL_MIN =               1 # Minimum base price for local resources  # 
PRICE_LOCAL_MAX =              10 # Maximum base price for local resources  # 
PRICE_FOREIGN_MIN =            10 # Minimum base price for remote resources # 
PRICE_FOREIGN_MAX =            20 # Maximum base price for remote resources # 
CIV_ANGER_RAND_MAX =           15 # Maximum attitude loss when being rude   #
CIV_HAPPY_RAND_MAX =           10 # Maximum attitude gain when being polite #
CIV_DAM_MIN =                  10 # Minimum damage done by civ defenses     # 
CIV_DAM_MAX =                  33 # Maximum damage done by civ defenses     # 

PLAYER_BASE_DAM_MIN =           3 # Base Minimum damage done by player      #
PLAYER_BASE_DAM_MAX =          12 # Base Maximum damage done by player      #

################################################################## Civilization:
class Civilization():
    '''
    attitude   -- The civilizations attitude toward player as a percentage.
    fiendlyMin -- Minimum attitude for civilization to remain friendly.
    enemyMax   -- Civilization will be hostile until attitude reaches this max.
    ty         -- Host planet type index.
    '''
    def __init__(self,ty,fri=ATTITUDE_FRIEND_MIN_DEFAULT,foe=ATTITUDE_ENEMY_MAX_DEFAULT):
        self.fiendlyMin = fri ; self.enemyMax = foe ; self.ty = ty
        self.attitude = random.randint(ATTITUDE_RAND_MIN,ATTITUDE_RAND_MAX)
        self.price = {}
        for i in range (len(resourceType[self.ty])):
            self.price[resourceType[self.ty][i]] = random.randint(PRICE_LOCAL_MIN,PRICE_LOCAL_MAX)
        #TODO: Add remote resources for trade with higher prices by default
    def Attitude(self,op=0):
        ''' Returns attitude string, and/or optionally modifies attitude.'''
        self.attitude += op
        if   self.attitude >= self.fiendlyMin:  return "Friendly"
        elif self.attitude >= self.enemyMax:    return "Neutral"
        else:                                   return "Hostile"
    def updatePrices(self): #TODO: Do this sometimes
        keys = list(self.price.keys())
        for i in range (len(keys)):
            adj = 0
            if keys[i] not in resourceType[self.ty]:
                adj += random.randint(RND_PRICE_ADJ_MIN,RND_PRICE_ADJ_MAX)
            if random.randint(0,100) < self.civ.attitude:
                  adj -= random.randint(ATTITUDE_PRICE_ADJ_MIN,ATTITUDE_PRICE_ADJ_MAX)
            else: adj += random.randint(ATTITUDE_PRICE_ADJ_MIN,ATTITUDE_PRICE_ADJ_MAX)
            self.price[keys[i]] += adj
    def attack(self,dam):
        self.attitude -= random.randint(1,CIV_ANGER_RAND_MAX) * random.randint(1,dam) #TODO Tune
        if self.attitude < 0: self.attitude = 0
        return int(random.randint(CIV_DAM_MIN,CIV_DAM_MAX)*(100-self.attitude)/100)
    def refine(self,amt,item):
        result = {}
        if item in refineConversions:
            if self.attitude >= self.fiendlyMin:
                result[refineConversions[item]] = int(amt*2/3)
            elif self.attitude >= self.enemyMax:
                result[refineConversions[item]] = int(amt*1/2)
            else:
                result[refineConversions[item]] = int(amt*1/3)
                if random.randint(1,100) > self.attitude:
                    result["Damage"] = random.randint(CIV_DAM_MIN,CIV_DAM_MAX)
        else: result[item] = amt
        return result
                
##################################################################### Resources:
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
    def __init__(self,civ_chance=DEFAULT_CIV_SPAWN_CHANCE):
        r = random.randint(0,planetTypeQt)
        self.res  = resourceType[r] ; self.type = planetType[r]
        if random.randint(1,100) in range (1, civ_chance):
                self.civ = Civilization(r) #TODO: Use fri,foe params
        else:   self.civ = None
        (self.harvest_chance_poor,self.harvest_chance_avg,
         self.harvest_poor_min,self.harvest_poor_max,
         self.harvest_avg_min,self.harvest_avg_max,
         self.harvest_good_min,self.harvest_good_max) = resouceChances[r]
    def harvest(self,bonus=0):
        '''Returns {'resource':quantity}. Assumes planet has verified success.'''
        result = {}
        if self.civ != None:
            if self.civ.Attitude(-random.randint(0,CIV_ANGER_RAND_MAX)) == "Hostile":
                result['Damage'] = random.randint(CIV_DAM_MIN,CIV_DAM_MAX) #TODO: apply modifiers
        chance = random.randint(0,100) #TODO: Get More Resources at a time?
        if chance <= self.harvest_chance_poor:
            result[min(self.res)] = random.randint(self.harvest_poor_min,self.harvest_poor_max) + bonus
        elif chance <= self.harvest_chance_avg:
            result[self.res[random.randint(0,len(self.res)-1)]] = random.randint(self.harvest_avg_min,self.harvest_avg_max) + bonus
        else: result[max(self.res)] = random.randint(self.harvest_good_min,self.harvest_good_max) + bonus
        return result
    def buy(self,item):
        '''Returns the price per item, 0 if item is unavialable, or damage.'''
        if self.civ == None: return 0
        if self.civ.Attitude() == "Hostile":
            if random.randint(0,100) > self.civ.attitude:
                if random.randint(0,100) < self.civ.attitude:
                    self.civ.attitude += random.randint(0,CIV_HAPPY_RAND_MAX)
                else:
                    value = random.randint(0,CIV_ANGER_RAND_MAX)
                    self.civ.attitude -= value
                    return value
        return self.civ.price.get(item,0)
    def attack(self,low=PLAYER_BASE_DAM_MIN,high=PLAYER_BASE_DAM_MAX):
        damRecv = 0 ; damDone = random.randint(low,high)
        if self.civ != None: damRecv += self.civ.attack(damDone)
        return (damDone,damRecv)
