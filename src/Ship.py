#!/usr/bin/python

import random
from Planets import System

################################################################################
#                                                                              #
# Ship.py -- The Spaceship                                                     #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

##################################################################### Constants:
# Starting Fuel #
INIT_FUEL_MIN = 0
INIT_FUEL_MAX = 100

# Distance From Home (Light Years) #
INIT_DIST_MIN = 1
INIT_DIST_MAX = 100
INIT_DIST_MULTIPLIER = 1000

# Traveling Distances #
DRIFT_DIST_MIN = 3
DRIFT_DIST_MAX = 15
HEAD_DIST_MIN = 1
HEAD_DIST_MAX = 10

# Fuel (percentage) Gained from Drifing #
DRIFT_FUEL_GAIN_MIN = 1
DRIFT_FUEL_GAIN_MAX = 10

MAX_PLANETS = 6

#################################################################### Ship Class:
class Ship():
    '''
    fuel    -- Percentage of fuel tank full.
    health  -- Percentage of ship hull integrity.
    cargo   -- Dictionary of resources.
    delta   -- Distance from home.
    heading -- Toward home or away? (+1 vs -1)
    sys     -- The current system.
    time    -- Time taken to get home.
    '''
    def __init__(self):
        self.fuel = random.randint(INIT_FUEL_MIN,INIT_FUEL_MAX)
        self.delta = random.randint(INIT_DIST_MIN,INIT_DIST_MAX)*INIT_DIST_MULTIPLIER
        self.sys = System(MAX_PLANETS)
        self.health = 100 ; self.time = 0 ; self.heading = 0
        while self.heading == 0: self.heading = random.randint(-1,1)
        self.cargo = {}
    def fuelerize(self,qt):
        '''Adjust fuel level by qt.'''
        self.fuel += qt
        if self.fuel > 100: self.fuel = 100;
        if self.fuel < 0:   self.fuel = 0;
    def depart(self,cost,dist):
        '''Depart the current system. Return TRUE if arrived at Home.'''
        self.fuelerize(cost) ; self.delta -= self.heading * dist 
        if self.delta <= 0:   return True
        self.sys = System(MAX_PLANETS) ; return False
    def drift(self):
        '''Depart the System while not only preserving fuel but accumulating it.'''
        tval = self.depart(
             random.randint(DRIFT_FUEL_GAIN_MIN,DRIFT_FUEL_GAIN_MAX),
             random.randint(DRIFT_DIST_MIN,DRIFT_DIST_MAX) )
        self.heading = 0
        while self.heading == 0: self.heading = random.randint(-1,1)
        return tval
    def goHome(self):
        if self.fuel > 0:
            self.heading = 1
            return self.depart(-self.fuel,self.fuel*random.randint(HEAD_DIST_MIN,HEAD_DIST_MAX))
        return false
    def orbit(self,index):
        self.sys.orbit(index)
    def harvest(self):
        #TODO: Pass through any Modifiers
        result = self.sys.harvest()
        if result != None:
            res_len = len(result)
            res_keys = result.keys()
            for i in range (0,res_len):
                if res_keys[i] == "Damage":
                    if not self.harm(result['Damage']): return False # Died #
                elif res_keys[i] not in self.cargo:
                        self.cargo[res_keys[i]]  = result[res_keys[i]]
                else:   self.cargo[res_keys[i]] += result[res_keys[i]]
        return True # Still Alive #
    def harm(self,amt):
        self.health -= amt
        if self.health <= 0: return False
        else:                return True    # Still Alive 
############################################################## Main for Testing:
if __name__ == '__main__':
    USSEnterprise = Ship()
    print "Ship:\n\tDistance Home:\t{} Light Years\n\tHull Integrity:\t{}%\n\tFuel:\t{}%".format( 
        USSEnterprise.delta, USSEnterprise.health, USSEnterprise.fuel )

