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
    '''Implements a Command Line version of The Game.'''
    def __init__(self,run=True):
        self.drifter = Ship.Ship()
        if run: self.main()
    def backstory(self):
        '''Return the backstory string.'''
        string = ('#' * 80) + "\n" #TODO: Add more randomized flavour.
        string += "The last thing you remember before awaking from chryostasis,"
        string += " was the captain\nbeing decapitated by some flying debris. "
        string += "There was a battle. You don't know if\nthe enemy was destroyed,"
        string += " but obviously your ship is intact. The onboard computer\n"
        string += "reports that you have been in stasis for {} years. ".format(random.randint(99,666))
        string += "The ship has been drifting\nthe entire time. You are lost, "
        string += "but the solar sails are functional.\n\n"
        string += "You may return to stasis and allow the ship to drift at any time. "
        string += "Or, if you\nhave fuel, you can head toward home. "
        if self.drifter.sys.qt > 0: string += "Perhaps one of these nearby planets has\n"
        else: string += "If you happen upon a solar system with\nplanets, perhaps you may find "
        string += "something interesting. A scan of the surface will occur automatically when you\nachieve orbit.\n"
        string += "\nIf you are still confused type 'help' at the prompt.\n"
        return string
    def commands(self):
        '''Enumerate available commands into a string.'''
        string =               "Available commands are: drift"
        if   self.drifter.fuel > 0:        string += ", head home"
        if   self.drifter.sys.pos != None: string += ", harvest, depart"
        elif self.drifter.sys.qt > 0:      string += ", orbit"
        if   len(self.drifter.cargo) > 0:  string += ", jettison"
        #TODO: Add More Commands: buy, sell, trade, fight, flee, ...
        string += ", and quit."
        return string
    def wingame(self):
        #TODO: Calculate Score -- Compare to High Score List
        print ('#' * (80-9), "YOU WIN!")    ;  sys.exit(0)
    def losegame(self):
        print ('#' * (80-11), "YOU LOOSE!") ;  sys.exit(0)
    def status(self):
        '''Create status string.'''
        return "[T:{}|D:{}|F:{}|H:{}|P:{}]".format(
                self.drifter.time, self.drifter.delta,
                self.drifter.fuel, self.drifter.health,
                self.drifter.sys.qt               )
    def listCargo(self):
        return "Cargo[{}%]:{}".format(
                int(100*(self.drifter.usedcap/self.drifter.cap)),
                self.drifter.cargo   )
    def main(self):
        ''' Play The Game. '''
        print(self.backstory())
        while True:
            print (self.commands(),"\n",self.listCargo())
            cmdLine = raw_input(self.status()+" What will you do? ").split()
            cmd = cmdLine[0] ; print ('#' * 80)
            
            ############################################################## Help:
            if cmd == "help":
                print ("\nThe ship status is described as so:\n"
                      +"\tT:time|D:distance|F:fuel|H:health|P:planets\n"
                      +"The planet scan is described as so:\n"
                      +"\t[type]{health}[resource,list]\n")
                continue
                
            ############################################################## Quit:
            if cmd == "quit":
                print ("\tSELF DESTRUCT SEQUENCE ACTIVATED!") ; self.losegame()
                
            ############################################################# Drift:
            if cmd == "drift":
                print ("You allow the space craft to drift...")
                if self.drifter.drift(): self.wingame()
                
            ######################################################### Head Home:
            if cmd == "head":
                print ("You set the ship autopilot to head home...")
                print ("You are awakened from chryostasis when the fuel runs out.")
                if self.drifter.goHome(): self.wingame()
                
            ########################################################### Harvest:
            if cmd == "harvest":
                print ("Harvesting...")
                if not self.drifter.harvest():
                    print ("You have been slain by the local civilization.")
                    self.losegame()
                
            ###################################################### Orbit Planet:
            if cmd == "orbit":
                try:
                    print ("Entering orbit of planet #{}".format(cmdLine[1]))
                    self.drifter.orbit(int(cmdLine[1]))
                    print ("Scan:",self.drifter.scan())
                except IndexError:
                    print ("?\n\tUsage: 'orbit n'") ; continue
                    
            ##################################################### Depart System:
            if cmd == "depart":
                print ("You leave the {} planet.".format(self.drifter.sys.pos))
                self.drifter.sys.pos = None
                
            #################################################### Jettison Cargo:
            if cmd == "jettison":
                try:
                    if cmdLine[2] == "Holy": cmdLine[2] = "Holy Water" #XXX#
                    print ("Jettisoning", cmdLine[1], cmdLine[2])
                    self.drifter.jettison(int(cmdLine[1]),cmdLine[2])
                except IndexError:
                    print ("?\n\tUsage: 'jettison n item'") ; continue
                    
            ####################################################################
            self.drifter.time += 1
            
            
# class GuiGame():


# class TwitterGame():


########################################################################## MAIN:
if __name__ == '__main__': game = CmdLineGame()
