#!/usr/bin/python3
################################################################################
#                                                                              #
# Drifter.py -- The Game Implementations                                       #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

import sys, random

sys.path.append("src/")
from src import Ship

raw_input = input #python3


##################################################################### Constants:
STASIS_YEARS_MIN = 99
STASIS_YEARS_MAX = 666

################################################################################
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
        string += "reports that you have been in stasis for {} years. ".format(
                              random.randint(STASIS_YEARS_MIN,STASIS_YEARS_MAX))
        string += "The ship has been drifting\nthe entire time. You are lost, "
        string += "but the solar sails are functional.\n\n"
        if self.drifter.credit < 0:
            string += "You have an overdue library fine of ${} universal credits.".format(-self.drifter.credit)
        string += "\n\nYou may return to stasis and allow the ship to drift at any time. "
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
        if self.drifter.sys.pos != None:
            if self.drifter.sys.planets[self.drifter.sys.pos].resources.civ != None:
                attitude = self.drifter.sys.planets[self.drifter.sys.pos].resources.civ.Attitude()
                if attitude != "Hostile":
                    string                        += ", buy, sell"
                    if attitude == "Friendly":
                        string                    += ", refine" #TODO
                string                            += ", attack" #TODO
            string                                += ", harvest, depart"
        elif self.drifter.sys.qt > 0:      string += ", orbit"
        if   len(self.drifter.cargo) > 0:  string += ", jettison"
        string += ", and quit."
        return string
    def wingame(self):
        #TODO: Calculate Score -- Compare to High Score List
        print ('#' * (80-9), "YOU WIN!\n")    ;  sys.exit(0)
    def losegame(self,string):
        print (string)
        print ('#' * (80-11), "YOU LOOSE!\n") ;  sys.exit(0)
    def status(self):
        '''Create status string.'''
        return "[T:{}|D:{}|F:{}|H:{}|P:{}|${}]".format(
                self.drifter.time,   self.drifter.delta,
                self.drifter.fuel,   self.drifter.health,
                self.drifter.sys.qt, self.drifter.credit)
    def listCargo(self):
        return "Cargo[{}%]:{}".format(
                int(100*(self.drifter.usedcap/self.drifter.cap)),
                self.drifter.cargo   )
    def main(self):
        ''' Play The Game. '''
        print(self.backstory())
        while True:
            print ("{}\n{}\nScan:{}".format(self.commands(),self.listCargo(),self.drifter.scan()))
            try:
                cmdLine = raw_input(self.status()+" What will you do? ").split()
                cmd = cmdLine[0] 
            except EOFError: cmd = "quit"
            
            print ("\n" +('#' * 80))
            
            ############################################################## Help:
            if cmd == "help": #TODO Add command parameter
                print ("\nThe ship status is described as so:\n\t"
                      +"[T:time|D:distance|F:fuel|H:health|P:planets|$credits]"
                      +"\nWhere time is how many turns have elapsed. "
                      +"Distance is how far from home you\nare. "
                      +"Planets indicate how many are in the current system. "
                      +"And credits is the\nbalance of your universal monetary exchange account. "
                      +"\n\nThe planet scan is described as so:\n\t"
                      +"[type]{health}[resource,list]\n")
                continue
                
            ############################################################## Quit:
            if cmd == "quit" or cmd = "exit" or cmd = "q":
                self.losegame("\tSELF DESTRUCT SEQUENCE ACTIVATED!")
                
            ############################################################# Drift:
            if cmd == "drift": #TODO Drifting while under attack is dangerous.
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
                    self.losegame("You have been slain by the local civilization.")
                
            ###################################################### Orbit Planet:
            if cmd == "orbit":
                try:
                    print ("Entering orbit of planet #{}".format(cmdLine[1]))
                    self.drifter.orbit(int(cmdLine[1]))
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
            
            ####################################################### Buy or Sell:
            if cmd == "buy" or cmd == "sell":
                try:
                    if cmdLine[2] == "Holy": cmdLine[2] = "Holy Water" #XXX#
                    if not self.drifter.shop(cmd,int(cmdLine[1]),cmdLine[2]):
                        self.losegame("While trying to make a deal to {} {} {}, you were seized and put to death.".format(cmd,cmdLine[1],cmdLine[2]))
                    else: print ("You {} some {}.".format(cmd,cmdLine[2]))
                except IndexError:
                    print ("?\n\tUsage: 'nuy n item'") ; continue

            ############################################################ Attack:
            if cmd == "attack":
                if not self.drifter.harm(self.drifter.sys.attack()):
                    self.losegame("Your ship was destroyed in battle.")

            ####################################################################
            self.drifter.time += 1
            
            
# class GuiGame():


# class TwitterGame():


########################################################################## MAIN:
if __name__ == '__main__': game = CmdLineGame()
