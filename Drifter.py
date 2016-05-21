#!/usr/bin/env python
################################################################################
#                                                                              #
# Drifter.py -- The Twitter Game Implementation                                #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

import datetime, io, random, sys, time

import twitter

sys.path.append("src/")
from src import Ship

#Dirty hack to rewrite print() -> string
# REALSTDOUT = sys.stdout
# sys.stdout = io.StringIO()

# def getPrintValue():
#     strValue = sys.stdout.getvalue()
#     sys.stdout = io.StringIO()
#     return strValue

# def dprint(*args):
#     tmp = sys.stdout
#     sys.stdout = sys.stderr
#     print("DEBUG:")
#     for a in args:
#         print(args)
#         sys.stdout.flush()
#     sys.stdout = tmp

dprint = print

##################################################################### Constants:
STASIS_YEARS_MIN = 99
STASIS_YEARS_MAX = 666

################################################################################
class TwitterGame():
    '''Implements a Twitter version of The Game.'''
    def __init__(self,run=True):
        self.drifter = Ship.Ship()
        self.twitter = twitter.Twitter('zmcbot')

        if run: self.main()
    def commands(self):
        '''Enumerate available commands into a string.'''
        msg =                                     "Available commands are: drift"
        if   self.drifter.fuel > 0:        msg += ", head home"
        if self.drifter.sys.pos != None:
            if self.drifter.sys.planets[self.drifter.sys.pos].resource.civ != None:
                attitude = self.drifter.sys.planets[self.drifter.sys.pos].resource.civ.Attitude()
                if attitude != "Hostile":
                    msg                        += ", buy, sell"
                    if attitude == "Friendly":
                        msg                    += ", refine, gamble"
                msg                            += ", attack"
            msg                                += ", harvest, depart"
        elif self.drifter.sys.qt > 0:      msg += ", orbit"
        if   len(self.drifter.cargo) > 0:  msg += ", jettison"
        msg += ", and quit."
        return msg
    def wingame(self):
        #TODO: Calculate Score -- Compare to High Score List
        print ('#' * (80-9) + " YOU WIN!\n")    ;  sys.exit(0)
    def losegame(self,msg):
        print (msg)
        print ('#' * (80-10) + " YOU LOSE!\n")    ;  sys.exit(0)
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
    def holyWaterHack(self,msg): #XXX#
        ''' XXX Change "Holy" to "Holy Water XXX"'''
        if msg == "Holy": return "Holy Water"
        else:                return  msg
    def main(self):
        ''' Play The Game. '''

        dispTop5 = True

        while True:
            #msg = getPrintValue()
            #dprint('This would get tweeted:\n', msg, 'Which is %d characters.\n' % len(msg))

            dprint("{}\n{}\nScan:{}".format( self.commands(),
                                             self.listCargo(),
                                             self.drifter.sys.scan() ))

            x = 1.5
            dprint("Sleeping for %.1f minutes...\n" % x)
            time.sleep(x * 60)

            dprint("I have awoken! Time to read the tweetmails!\n")

            tweets = self.twitter.getTweets()
            top5 = self.twitter.findTop5Votes()

            if dispTop5:
                #Only display the top 5, don't execute them
                dprint("Top 5 tweeted commands:\n", top5)
            else:
                #Run the top voted command!
                if len(top5) > 0:
                    cmdLine = top5[0][0].split()
                    cmd = cmdLine[0]
                else:
                    cmdLine = ('drift',)
                    cmd = 'drift'
                #TODO: Set the "success" flag to True for the winning tweets, then...
                #TODO: Save these tweets to a database before deleting them
                self.twitter.resetTweets()

            #Toggle display/execute
            dispTop5 = (not dispTop5)

            if not dispTop5:
                continue

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
                    self.drifter.sys.orbit(int(cmdLine[1])-1)
                except (IndexError, ValueError):
                    print ("?\n\tUsage: 'orbit n'") ; continue

            ##################################################### Depart System:
            if cmd == "depart": #XXX Not Necessary XXX#
                print ("You leave the {} planet.".format(self.drifter.sys.pos+1))
                self.drifter.sys.pos = None

            #################################################### Jettison Cargo:
            if cmd == "jettison":
                try:
                    cmdLine[2] = self.holyWaterHack(cmdLine[2])
                    print ("Jettisoning", cmdLine[1], cmdLine[2])
                    self.drifter.jettison(int(cmdLine[1]),cmdLine[2])
                except (IndexError, ValueError):
                    print ("?\n\tUsage: 'jettison n item'") ; continue

            ####################################################### Buy or Sell:
            if cmd == "buy" or cmd == "sell":
                try:
                    cmdLine[2] = self.holyWaterHack(cmdLine[2])
                    if not self.drifter.shop(cmd,int(cmdLine[1]),cmdLine[2]):
                        self.losegame("While trying to make a deal to {} {} {}".
                             format(cmd,cmdLine[1],cmdLine[2])
                            +", you were seized and put to death.")
                    else: print ("You {} some {}.".format(cmd,cmdLine[2]))
                except (IndexError, ValueError):
                    print ("?\n\tUsage: '{} n item'".format(cmd)) ; continue

            ############################################################ Attack:
            if cmd == "attack":
                if not self.drifter.harm(self.drifter.sys.attack()):
                    self.losegame("Your ship was destroyed in battle.")

            ############################################################ Refine:
            if cmd == "refine":
                try:
                    cmdLine[2] = self.holyWaterHack(cmdLine[2])
                    if not self.drifter.refine(int(cmdLine[1]),cmdLine[2]):
                        self.losegame("You were caught tresspassing in "
                            +  "the refinery, seized, and put to death.")
                except (IndexError, ValueError):
                    print ("?\n\tUsage: 'refine n item'") ; continue

            ############################################################ Gamble:
            if cmd == "gamble":
                try:
                    if not self.drifter.gamble(int(cmdLine[1])):
                        self.losegame("Another gambler accused you of cheating."
                            + ", you have been seized and put to death.")
                except (IndexError, ValueError):
                    print ("?\n\tUsage: 'gamble bet'") ; continue

            ####################################################################
            self.drifter.time += 1

########################################################################## MAIN:
if __name__ == '__main__': TwitterGame()
