#!/usr/bin/python
################################################################################
#                                                                              #
# DrifterGui.py -- The Graphical Game Implementation                           #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

import random, sys, time

import pygame

sys.path.append("src/")
from src import Ship, Graphics

##################################################################### Constants:
STASIS_YEARS_MIN = 99
STASIS_YEARS_MAX = 666

# COMMANDS #
CMD_QUIT       = pygame.K_q
CMD_HEAD_HOME  = pygame.K_z
CMD_DRIFT      = pygame.K_x
CMD_DEPART     = pygame.K_0
CMD_ORBIT_1    = pygame.K_1
CMD_ORBIT_2    = pygame.K_2
CMD_ORBIT_3    = pygame.K_3
CMD_ORBIT_4    = pygame.K_4
CMD_ORBIT_5    = pygame.K_5
CMD_ORBIT_6    = pygame.K_6
CMD_HARVEST_X  = 240           # Click on rectangular region within Planet.
CMD_HARVEST_Y  = 275
#CMD_JETTISON  = pygame.K_j
#CMD_BUY       = pygame.K_b
#CMD_SELL      = pygame.K_s
#CMD_REFINE    = pygame.K_r
#CMD_GAMBLE    = pygame.K_g
#CMD_ATTACK    = pygame.K_a

################################################################################
#TODO: print --> self.print : write to ship's console. Also create ships console
class GuiGame():
    '''Implements a Graphical version of The Game.'''
    def __init__(self,name="Testing",run=True):
        self.name    = name
        self.drifter = Ship.Ship()
        self.gfx     = Graphics.Graphics(self.name,self.drifter)
        self.starChart = None
        if run: self.main()
    def render(self):
        self.gfx.scene_gen(self.starChart) ; pygame.display.flip()
    def orbit(self,ix):
        if ix < 1 or ix >= self.drifter.sys.qt: self.drifter.sys.pos = None
        else:                                   self.drifter.sys.orbit(ix)
    def main(self):
        self.render()
        while True:
            something_happened = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if event.type == pygame.KEYDOWN:
                    cmd = event.key

                    ###################################################### Quit:
                    if cmd == CMD_QUIT: return

                    ##################################################### Drift:
                    if cmd == CMD_DRIFT:
                        something_happened = True ; self.starChart = None
                        print ("You allow the space craft to drift...")
                        if self.drifter.drift(): pass #self.wingame()

                    ################################################# Head Home:
                    if cmd == CMD_HEAD_HOME:
                        something_happened = True ; self.starChart = None
                        print ("You set the ship autopilot to head home...")
                        print ("You are awakened from chryostasis when the fuel runs out.")
                        if self.drifter.goHome(): pass #self.wingame()

                    ############################################## Orbit Planet:
                    if cmd == CMD_ORBIT_1: self.orbit(1) ; something_happened = True
                    if cmd == CMD_ORBIT_2: self.orbit(2) ; something_happened = True
                    if cmd == CMD_ORBIT_3: self.orbit(3) ; something_happened = True
                    if cmd == CMD_ORBIT_4: self.orbit(4) ; something_happened = True
                    if cmd == CMD_ORBIT_5: self.orbit(5) ; something_happened = True
                    if cmd == CMD_ORBIT_6: self.orbit(6) ; something_happened = True

                    ############################################# Depart System:
                    if cmd == CMD_DEPART:  self.orbit(0) ; something_happened = True
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (x,y) = event.pos
                    
                    ################################################### Harvest:
                    if x <= CMD_HARVEST_X and y <= CMD_HARVEST_Y:
                        something_happened = True
                        print ("Harvesting...")
                        if not self.drifter.harvest():
                            pass #self.losegame("You have been slain by the local civilization.")

                ################################################################
                if something_happened:
                    self.drifter.time += 1 ; self.render()
        pygame.quit()


########################################################################## MAIN:
if __name__ == '__main__': GuiGame()#time.asctime())
