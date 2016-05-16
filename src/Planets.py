#!/usr/bin/python

import random

from Cargo import Resource, planetTypeQt, DEFAULT_CIV_CHANCE

################################################################################
#                                                                              #
# Planets.py -- Planets and Solar Systems                                      #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

##################################################################### Constants:
MAX_BASE_CHANCE = 66
MIN_HEALTH = 25

################################################################## Planet Class:
class Planet():
    '''
    resources   -- Civilization and Resources on Planet.
    health      -- Remaining population, or resources, if any.
    baseChance  -- Base chance for gathering, fighting, etc.
    '''
    def __init__(self,civ_chance = DEFAULT_CIV_CHANCE):
        self.resources = Resource(civ_chance)
        self.health = random.randint(MIN_HEALTH,100)
        self.baseChance = random.randint(0,MAX_BASE_CHANCE)
    def harvest(self,adj = 0, bonus = 0):
        if self.health > 0: #TODO: Possibly harm planet's health
            if (adj + random.randint(1,100)) > self.baseChance:
                return self.resources.harvest(bonus)
        return None
            
    #def buy(self,resource):
    #def sell(self,resource):
    #def trade(self,want,have):
    

        
################################################################## System Class:
class System():
    '''
    qt -- Quantity of planets in this system.
    planets -- List of planets in this system.
    pos -- Index of which planet is being orbited? or None
    '''
    def __init__(self,maxQt,civ_chance = DEFAULT_CIV_CHANCE):
        self.qt = random.randint(0,maxQt)
        self.planets = []
        for i in range (0, self.qt): self.planets.append(Planet(civ_chance))
        self.pos = None
    def orbit(self,idx):
        if(( idx >= 0 )and( idx < self.qt )): self.pos = idx
    def scan(self):
        string = ""
        if self.pos != None:
            string += '['
            if self.planets[self.pos].resources.civ != None:
                string += "Civilized " + self.planets[self.pos].resources.civ.Attitude() + ' '
            string +=       self.planets[self.pos].resources.type
            string += ']'
            string += '{' + str(self.planets[self.pos].health)        + '}'
            string +=       str(self.planets[self.pos].resources.res)
        return string
    def harvest(self,adj=0,bonus=0):
        if self.pos != None: return self.planets[self.pos].harvest(adj,bonus)
        else: return None #TODO: Solar scoop? gain fuel without leaving system.

############################################################## Main for Testing:
if __name__ == '__main__':
    max_planets = 6
    sys = System(max_planets)
    
