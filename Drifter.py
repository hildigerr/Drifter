#!/usr/bin/python3

import sys, random

sys.path.append("src/")
from src import Ship

################################################################################
#                                                                              #
# Ship.py -- The Spaceship                                                     #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

raw_input = input #python3

class CmdLineGame():
    def __init__(self):
        self.drifter = Ship.Ship()
        self.main()
    def backstory(self):
        print ('#' * 80)
        string  = "The last thing you remember before awaking from chryostasis, was the captain\nbeing decapitated by some flying debris. "
        string += "There was a battle. You don't know if\nthe enemy was destroyed, but obviously your ship is intact. "
        string += "The onboard computer\nreports that you have been in stasis for {} years. ".format(random.randint(99,666))
        string += "The ship has been drifting\nthe entire time. You are lost, but the solar sails are functional.\n"
        print (string)
        string  = "You may return to stasis and allow the ship to drift at any time. Or, if you\nhave fuel, you can head toward home. "
        if self.drifter.sys.qt > 0: string += "Perhaps one of these nearby planets has\n"
        else: string += "If you happen upon a solar system with\nplanets, perhaps you may find "
        string += "something interesting. A scan of the surface will occur automatically when you\nachieve orbit.\n"
        print (string)
    def commands(self):
        string =             "Available commands are: drift"
        if   self.drifter.fuel > 0:        string += ", head home"
        if   self.drifter.sys.pos != None: string += ", harvest, depart"
        elif self.drifter.sys.qt > 0:      string += ", orbit"
        if   len(self.drifter.cargo) > 0:  string += ", jettison"
        string += ", and quit."
        print (string)
    def wingame(self):
        print ('#' * (80-9), "YOU WIN!")    ;  sys.exit(0)
    def losegame(self):
        print ('#' * (80-11), "YOU LOOSE!") ;  sys.exit(0)
    def status(self):
        print ("T:{}|D:{}|F:{}|H:{}|P:{}\nCargo:{}".format(
                                                 self.drifter.time,
                                                 self.drifter.delta,
                                                 self.drifter.fuel,
                                                 self.drifter.health,
                                                 self.drifter.sys.qt,
                                                 self.drifter.cargo ))
    def main(self):
        self.backstory()
        while True:
            self.status() ; self.commands()
            cmdLine = raw_input("What will you do? ").split(); cmd = cmdLine[0]
            print ('#' * 80)
            if cmd == "quit":
                print ("\tSELF DESTRUCT SEQUENCE ACTIVATED!") ; self.losegame()
            if cmd == "drift":
                print ("You allow the space craft to drift...")
                if self.drifter.drift(): self.wingame()
            if cmd == "head":
                print ("You set the ship autopilot to head home...")
                print ("You are awakened from chryostasis when the fuel runs out.")
                if self.drifter.goHome(): self.wingame()
            if cmd == "harvest":
                print ("Harvesting...")
                if not self.drifter.harvest():
                    print ("You have been slain by the local civilization.")
                    self.losegame()
            if cmd == "orbit":
                try:
                    print ("Entering orbit of planet "), cmdLine[1]
                    self.drifter.orbit(int(cmdLine[1]))
                except IndexError:
                    print ("?\n\tUsage: 'orbit n'") ; continue
            if cmd == "depart":
                print ("You leave the {} planet.").format(self.drifter.sys.pos)
                self.drifter.sys.pos = None
            if cmd == "jettison":
                try:
                    print ("Jettisoning", cmdLine[1], cmdLine[2])
                    self.drifter.jettison(int(cmdLine[1]),cmdLine[2])
                except IndexError:
                    print ("?\n\tUsage: 'jettison n item'") ; continue
            self.drifter.time += 1
            
            
# class GuiGame():


# class TwitterGame():


########################################################################## MAIN:
if __name__ == '__main__': game = CmdLineGame()
