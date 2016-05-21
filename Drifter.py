#!/usr/bin/env python
################################################################################
#                                                                              #
# Drifter.py -- The Twitter Game Implementation                                #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

#System libraries
import datetime, io, random, sys, time

#Extra libraries
import pygame, twitter

#Game libraries
sys.path.append("src/")
from src import Ship, Graphics
from DrifterCmd import *

##################################################################### Constants:

################################################################################
class TwitterGame():
    '''Implements a Twitter version of The Game.'''
    def __init__(self,name="Testing",run=True):
        self.name = name
        self.drifter = Ship.Ship()
        self.twitter = twitter.Twitter(self.name)
        self.command = CmdLineGame(False,self.drifter)
        self.gfx     = Graphics.Graphics(self.name,self.drifter,self.command.backstory()+"\n\n"+self.command.commands())
        self.starChart = None
        if run: self.main() ; pygame.quit()

    def render(self):
        print("DEBUG... Rendering") #TODO: Ensuring no extra rendering occurs.
        self.imgFileName  = self.gfx.scene_gen(self.starChart)
        pygame.display.flip()

    def main(self):
        ''' Play The Game. '''
        dispTop5 = True #Flag to say if we simply display the top 5, or run the top command
        result = None
        status = GAME_CONTINUE

        while True:
            self.render()

            print("Sending tweet with image...",)
            self.twitter.sendTweet('', self.imgFileName)
            print("Sent!")

            x = 1.5
            print("Sleeping for %.1f minutes...\n" % x)
            time.sleep(x * 60)

            print("I have awoken! Time to read the tweetmails!\n")

            tweets = self.twitter.getTweets()
            top5 = self.twitter.findTop5Votes()

            if dispTop5:
                #Only display the top 5, don't execute them
                print("Top 5 tweeted commands:\n", top5)
            else:
                #Run the top voted command!
                if len(top5) > 0:
                    cmdLine = top5[0][0].split()
                    cmd = cmdLine[0]
                else:
                    cmdLine = ('drift',)
                    cmd = 'drift'

                #Flag the winning votes
                if len(top5) > 0:
                    self.twitter.setSuccess(top5[0][0])

                #TODO: Save these tweets to a database before deleting them
                self.twitter.resetTweets()

            #Toggle display/execute
            dispTop5 = (not dispTop5)
            #We just displayed the top 5, we didn't actually run a command
            #Just go back to the loop and sleep again
            if not dispTop5:
                self.gfx.txt = ( self.twitter.top5ToString(top5)
                                 + "\n\n" + self.command.listCargo()
                                 + "\n\n" + self.command.commands() )
                continue

            #Some commands require us to update the star chart, most do not

            ############################################################# Drift:
            if cmd == "drift": #TODO Drifting while under attack is dangerous.
                self.starChart = None
                (result, status) = self.command.do(["drift"])

            ######################################################### Head Home:
            elif cmd == "head":
                self.starChart = None
                (result,status) = self.command.do(["head"])

            ################################################### Everything else:
            else:
                (result,status) = self.command.do(cmdLine)

            ####################################################################
            if result != None:
                self.gfx.txt = ( self.twitter.top5ToString(top5)
                                 + result
                                 + "\n\n" + self.command.listCargo()
                                 + "\n\n" + self.command.commands() )
                self.render()

            if status == GAME_TERMINATE: return
            if status != GAME_CONTINUE:  self.drifter.time += 1

########################################################################## MAIN:
if __name__ == '__main__': TwitterGame('zmcbot')