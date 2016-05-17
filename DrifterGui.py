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
#CMD_BUY       = pygame.K_b
#CMD_SELL      = pygame.K_s
#CMD_REFINE    = pygame.K_r
#CMD_GAMBLE    = pygame.K_g
#CMD_ATTACK    = pygame.K_a
#CMD_HARVEST   = pygame.K_h
CMD_DEPART    = pygame.K_0
CMD_ORBIT_1   = pygame.K_1
CMD_ORBIT_2   = pygame.K_2
CMD_ORBIT_3   = pygame.K_3
CMD_ORBIT_4   = pygame.K_4
CMD_ORBIT_5   = pygame.K_5
CMD_ORBIT_6   = pygame.K_6
#CMD_JETTISON  = pygame.K_j

################################################################################
class GuiGame():
    '''Implements a Graphical version of The Game.'''
    def __init__(self,name="Testing",run=True):
        self.name    = name
        self.drifter = Ship.Ship()
        self.screen  = pygame.display.set_mode(Graphics.SCREEN_SIZE)
        if run: self.main()
    def render(self):
        self.screen = Graphics.scene_gen(self.name,self.drifter,self.screen)
        pygame.display.flip()
    def orbit(self,ix):
        if ix < 1:  self.drifter.sys.pos = None
        else:       self.drifter.sys.orbit(ix)
    def main(self):
        self.render()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if event.type == pygame.KEYDOWN:
                    if event.key == CMD_QUIT: return
                    if event.key == CMD_HEAD_HOME:
                        print ("You set the ship autopilot to head home...")
                        print ("You are awakened from chryostasis when the fuel runs out.")
                        if self.drifter.goHome(): pass #self.wingame()
                    elif event.key == CMD_DRIFT:
                        print ("You allow the space craft to drift...")
                        if self.drifter.drift(): pass #self.wingame()
                    elif event.key == CMD_ORBIT_1: self.orbit(1)
                    elif event.key == CMD_ORBIT_2: self.orbit(2)
                    elif event.key == CMD_ORBIT_3: self.orbit(3)
                    elif event.key == CMD_ORBIT_4: self.orbit(4)
                    elif event.key == CMD_ORBIT_5: self.orbit(5)
                    elif event.key == CMD_ORBIT_6: self.orbit(6)
                    elif event.key == CMD_DEPART:  self.orbit(0)
                self.render()
        pygame.quit()


########################################################################## MAIN:
if __name__ == '__main__': GuiGame()#time.asctime())
