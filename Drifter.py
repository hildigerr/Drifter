#!/usr/bin/python

import sys, random
from src import Ship

################################################################################
#                                                                              #
# Ship.py -- The Spaceship                                                     #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################


class CmdLineGame():
    def __init__(self):
        self.drifter = Ship.Ship()
        self.main()
    def backstory(self):
        print '#' * 80
        string  = "The last thing you remember before awaking from chryostasis, was the captain\nbeing decapitated by some flying debris. "
        string += "There was a battle. You don't know if\nthe enemy was destroyed, but obviously your ship is intact. "
        string += "The onboard computerreports that you have been in stasis for {} years. ".format(random.randint(99,666))
        string += "The ship has been drifting\nthe entire time. You are lost, but the solar sails are functional.\n"
        print string
        string  = "You may return to stasis and allow the ship to drift at any time. Or, if you\nhave fuel, you can head toward home. "
        if self.drifter.sys.qt > 0: string += "Perhaps one of these nearby planets has\n"
        else: string += "If you happen upon a solar system with\nplanets, perhaps you may find "
        string += "something interesting. A scan of the surface will occur automatically when you\nachieve orbit.\n"
        print string
    def commands(self):
        string =             "Available commands are: drift"
        if self.drifter.fuel > 0:        string += ", head home"
        if self.drifter.sys.pos != None: string += ", harvest"
        if self.drifter.sys.qt > 0:      string += ", orbit"
        string += ", and quit."
        print string
    def wingame():
        print '#' * 80
        print "YOU WIN!"
        sys.exit(0)
    def status(self):
        print "T:{}|D:{}|F:{}|H:{}|P:{}".format( self.drifter.time,
                                                 self.drifter.delta,
                                                 self.drifter.fuel,
                                                 self.drifter.health,
                                                 self.drifter.sys.qt )
    def main(self):
        self.backstory()
        while True:
            self.status() ; self.commands()
            cmdLine = raw_input("What will you do? "); cmd = cmdLine.split()[0]
            if cmd == "quit": sys.exit(0)
            if cmd == "drift":
                if self.drifter.drift(): self.wingame()
            if cmd == "head":
                if self.drifter.goHome(): self.wingame()
            if cmd == "harvest": self.drifter.harvest()
            if cmd == "orbit": self.drifter.orbit(int(cmdLine.split()[1]))
            self.drifter.time += 1
            
            
# class GuiGame():


# class TwitterGame():


########################################################################## MAIN:
if __name__ == '__main__': game = CmdLineGame()
