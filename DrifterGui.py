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

################################################################################
class GuiGame():
    '''Implements a Graphical version of The Game.'''
    def __init__(self,name="Testing",run=True):
        self.name   = name
        self.player = Ship.Ship()
        self.screen = pygame.display.set_mode(Graphics.SCREEN_SIZE)
        if run: self.main()
    def render(self):
        Graphics.scene_gen( self.name, self.player, self.screen )
        pygame.display.flip()
    def done(self):
        pygame.quit()
    def main(self):
        self.render()
        while True :
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
        self.done()


########################################################################## MAIN:
if __name__ == '__main__': GuiGame()#time.asctime())
