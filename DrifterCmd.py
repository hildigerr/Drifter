#!/usr/bin/python3
################################################################################
#                                                                              #
# DrifterCmd.py -- The Command Line Game Implementation                        #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

import random, sys, time

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
        string += " is the captain\nbeing decapitated by some flying debris. "
        string += "There was a battle. You don't know if\nthe enemy was destroyed,"
        string += " but obviously your ship is intact. The onboard computer\n"
        string += "reports that you have been in stasis for {} years. ".format(
                              random.randint(STASIS_YEARS_MIN,STASIS_YEARS_MAX))
        string += "The ship has been drifting\nthe entire time.\n\n"
        string += "You are {} light years from home, ".format(self.drifter.delta)
        string += "but the solar sails are functional.\n"
        if self.drifter.credit < 0:
            string += "You have an overdue library fine of ${} universal credits.\n".format(-self.drifter.credit)
        string += "\nYou may return to stasis and allow the ship to drift at any time. "
        string += "Or, if you\nhave fuel, you can head toward home. "
        if self.drifter.sys.qt > 0: string += "Perhaps one of these nearby planets has\n"
        else: string += "If you happen upon a solar system with\nplanets, perhaps you may find "
        string += "something interesting.\n"
        string += "\nIf you are still confused type 'help' at the prompt.\n"
        return string
    def commands(self):
        '''Enumerate available commands into a string.'''
        string =               "Available commands are: drift"
        if   self.drifter.fuel > 0:        string += ", head home"
        if self.drifter.sys.pos != None:
            if self.drifter.sys.planets[self.drifter.sys.pos].resource.civ != None:
                attitude = self.drifter.sys.planets[self.drifter.sys.pos].resource.civ.Attitude()
                if attitude != "Hostile":
                    string                        += ", buy, sell"
                    if attitude == "Friendly":
                        string                    += ", refine, gamble"
                string                            += ", attack"
            string                                += ", harvest, depart"
        elif self.drifter.sys.qt > 0:      string += ", orbit"
        if   len(self.drifter.cargo) > 0:  string += ", jettison"
        string += ", and quit.\n"
        return string
    def wingame(self):
        #TODO: Calculate Score -- Compare to High Score List
        print ('#' * (80-9) + " YOU WIN!\n")    ;  sys.exit(0)
    def losegame(self,string):
        print (string)
        print ('#' * (80-10) + " YOU LOSE!\n")  ;  sys.exit(0)
    def status(self):
        '''Create status string.'''
        return "[T:{}|D:{}|F:{}|H:{}|${}]".format(
                self.drifter.time,   self.drifter.delta,
                self.drifter.fuel,   self.drifter.health,
                self.drifter.credit              )
    def listCargo(self):
        return "Cargo[{}%]:{}".format(
                int(100*(self.drifter.usedcap/self.drifter.cap)),
                self.drifter.cargo   )
    def holyWaterHack(self,string): #XXX#
        ''' XXX Change "Holy" to "Holy Water" XXX'''
        if string == "Holy": return "Holy Water"
        else:                return  string
    def main(self):
        ''' Play The Game. '''
        print(self.backstory())
        while True:
            print ("{}\n{}\nScan:{}".format( self.commands(),
                                             self.listCargo(),
                                             self.drifter.sys.scan() ))
            try:
                cmdLine = raw_input(self.status()+" What will you do? ").split()
                cmd = cmdLine[0]
            except (EOFError) : continue #cmd = "quit"
            print ("\n" + ('#' * 80) + "\n" + self.do(cmd,cmdLine) )
            self.drifter.time += 1 #TODO: don't take a turn if cmd is rejected.
    def do(self,cmd,cmdLine):
            '''Perform a cmd and Return Result String, if not done.'''
            ############################################################## Help:
            if cmd == "help": #TODO Add command parameter
                return ("The ship status is described as so:\n\t"
                      +"[T:time|D:distance|F:fuel|H:health|$credits]"
                      +"\nWhere time is how many turns have elapsed. "
                      +"Distance is how far from home you\nare. "
                      +"Planets indicate how many are in the current system. "
                      +"And credits is the\nbalance of your universal monetary exchange account. "
                      +"\n\nThe planet scan is described as so:\n\t"
                      +"[i/n type]{health}[resource,list]"
                      +"\nWhere i is the number of the planet "
                      +"and n is quantity of planets in the system.\n")
                
            ############################################################## Quit:
            if cmd == "quit" or cmd == "exit" or cmd == "q":
                self.losegame("\tSELF DESTRUCT SEQUENCE ACTIVATED!")
                
            ############################################################# Drift:
            if cmd == "drift": #TODO Drifting while under attack is dangerous.
                if self.drifter.drift(): self.wingame()
                return "The space craft is allowed to drift into another solar system..."
                
            ######################################################### Head Home:
            if cmd == "head":
                if self.drifter.goHome(): self.wingame()
                return ("The ship autopilot is set to head home..." + "\n"
                    "You awaken from chryostasis when the fuel runs out.")
                
            ########################################################### Harvest:
            if cmd == "harvest":
                (alive,result) = self.drifter.harvest()
                if not alive: self.losegame("The local population rise against you and destroy the ship.")
                else: return "Harvesting...\nFound: {}".format(result)
                
            ###################################################### Orbit Planet:
            if cmd == "orbit":
                try:
                    self.drifter.sys.orbit(int(cmdLine[1])-1)
                    return ("Entering orbit of planet #{}".format(cmdLine[1]))
                except (IndexError, ValueError):
                    return ("?\n\tUsage: 'orbit n'")
                    
            ##################################################### Depart System:
            if cmd == "depart": #XXX Not Necessary XXX#
                old = self.drifter.sys.pos
                if old != None: old+=1
                self.drifter.sys.pos = None
                return ("You leave the {} planet.".format(old))
                
            #################################################### Jettison Cargo:
            if cmd == "jettison":
                try:
                    cmdLine[2] = self.holyWaterHack(cmdLine[2])
                    cmdLine[1] = self.drifter.jettison(int(cmdLine[1]),cmdLine[2])
                    return ("Jettisoning {} {}".format(cmdLine[1], cmdLine[2]))
                except (IndexError, ValueError):
                    return ("?\n\tUsage: 'jettison n item'")
            
            ####################################################### Buy or Sell:
            if cmd == "buy" or cmd == "sell":
                try:
                    cmdLine[2] = self.holyWaterHack(cmdLine[2])
                    (alive,cmdLine[1]) = self.drifter.shop(cmd,int(cmdLine[1]),cmdLine[2])
                    if not alive:
                        self.losegame("While trying to make a deal to {} {} {}".
                             format(cmd,cmdLine[1],cmdLine[2])
                            +", you were seized and put to death.")
                    else: return ("You {} {} {}.".format(cmd,cmdLine[1],cmdLine[2]))
                except (IndexError, ValueError):
                    return ("?\n\tUsage: '{} n item'".format(cmd))

            ############################################################ Attack:
            if cmd == "attack":
                (damDone,damSustained) = self.drifter.sys.attack()
                if not self.drifter.harm(damDone):
                    self.losegame("Your ship was destroyed in battle.")
                else: return "You attack for {} damage, while sustaining {} damage.".format(damDone,damSustained)
                    
            ############################################################ Repair:
            #TODO: Use metal at friendly planet. 
            #      Not 1:1, and probably not random either. Tunable.

            ############################################################ Refine:
            if cmd == "refine": #TODO: Planet charges for this service?
                try:
                    cmdLine[2] = self.holyWaterHack(cmdLine[2])
                    (alive,result) = self.drifter.refine(int(cmdLine[1]),cmdLine[2])
                    if not alive: self.losegame("You were caught tresspassing in "
                            +  "the refinery, seized, and put to death.")
                    return "Refining {} {}...\nResult: {}".format(cmdLine[1],cmdLine[2],result)
                except (IndexError, ValueError):
                    return ("?\n\tUsage: 'refine n item'")

            ############################################################ Gamble:
            if cmd == "gamble":
                try:
                    (alive,result,dam) = self.drifter.gamble(int(cmdLine[1]))
                    if dam > 0: damage = "Another gambler accused you of cheating and attacks for {} damage!".format(dam)
                    else:       damage = ""
                    if not alive:
                        self.losegame("Another gambler accused you of cheating."
                            + " You have been seized and put to death.")
                    if result == None: return "You make a bet with yourself and win!"
                    if result < 0: return damage+"You gamble away {} credits!".format(-result)
                    else:          return damage+"You make a bet for {} and win {}".format(cmdLine[1],result)  
                except (IndexError, ValueError):
                    return ("?\n\tUsage: 'gamble bet'")

            ############################################################# Craft:
            if cmd == "craft":
                try:
                    self.drifter.craft(int(cmdLine[1]),cmdLine[2])
                except (IndexError, ValueError):
                    return ("?\n\tUsage: 'craft n item'")

            ############################################################### God:
            if cmd == "gm":
                self.drifter.gm()

            ####################################################################
            return "\"{}\" is an invalid command.".format(cmd) # self.do("drift",None)

########################################################################## MAIN:
if __name__ == '__main__': CmdLineGame()
