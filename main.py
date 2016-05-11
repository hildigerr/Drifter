# main.py:
# The main program that run the game bot

#Python Libraries
import sys, time, random

#Our libraries
#import gfx, twitter

'''
NOTES : 
========================================
in space:
goto
drift - no one votes, default action
head home

in planet :
harvest - has resources
trade - has civ
fight - has civ
leave - system

========================================
'''

class makePlanet (object):
   def __init__(node):
      node.planetNum = -1
      node.planetType = None
      node.resources = {}
      node.adjPlanets = []
      node.civ = None
      node.civHealth = None
      node.civStatus = None

class makeMilFalcon (object):
   def __init__(node):
      node.fuel = 100
      node.health = 100
      node.resources = {}
      node.damageMin = 8
      node.damageMax = 11
      node.currPlanet = None

def genPlanetResources (planet):
   index = 1
   resourceList = {}
   rockRes = {0:"Stones", 1:"Rocks", 2:"Dirt", 3:"Metals"}
   waterRes = {0:"Water", 1:"Ice", 2:"Holy Water"}
   fireRes = {0:"Obsidian", 1:"Lava", 2:"Diamond", 3:"Charcoal"}

   if (planet.planetType == "Rock"):
      for i in range (0, 3):
         currResource = rockRes[random.randint(0, 3)]
         if (currResource not in resourceList):
            resourceList.update({currResource:index})
   elif (planet.planetType == "Watr"):
      for i in range (0, 3):
         currResource = waterRes[random.randint(0, 2)]
         if (currResource not in resourceList):
            resourceList.update({currResource:index})
   elif (planet.planetType == "Fire"):
      for i in range (0, 3):
         currResource = fireRes[random.randint(0, 3)]
         if (currResource not in resourceList):
            resourceList.update({currResource:index})
   return resourceList

def generateMap ():
   universe =  []
   planetTypeOpt = {0:"Rock", 1:"Watr", 2:"Fire"}
   civOpt = {0:"Trading", 1:"Bandit"}

   for i in range (0, 100):
      planet = makePlanet()
      planet.planetNum = i
      planet.planetType = planetTypeOpt[random.randint(0, 2)]
      planet.resources = genPlanetResources(planet)

      if ((i+10) < 100):
         planet.adjPlanets.append(i+10)
      if ((i-10) > 0):
         planet.adjPlanets.append(i-10)
      if ((i%10) != 0):
         planet.adjPlanets.append(i-1)
      if (((i-9)%10) != 0):
         planet.adjPlanets.append(i+1)

      if (random.randint(0,99) in range (0, 49)):
         chosenCiv = random.randint(0,1)
         planet.civ = civOpt[chosenCiv]
         if (chosenCiv == 1):
            planet.civHealth = 55
         else:
            planet.civHealth = 70
         
      universe.append(planet)

   homePlanet = universe[random.randint(0, 9)]
   homePlanet.planetType = "HOME"

   startPlanet = universe[random.randint(90, 99)]
   startPlanet.planetType = "STRT"

   milFalcon = makeMilFalcon()
   milFalcon.currPlanet = startPlanet.planetNum

   return (milFalcon, universe)

def cmd_goto(gotoPlanet, milFalcon, universe):
   currentPlanet = milFalcon.currPlanet
   adjPlanets = universe[currentPlanet].adjPlanets

   if (gotoPlanet in adjPlanets):
      print("Travelling to Planet #", gotoPlanet, "...")
      milFalcon.currPlanet = gotoPlanet
      milFalcon.fuel = milFalcon.fuel - 10
   else:
      print("ERROR : Planet #", gotoPlanet, "is not adjacent.")

def cmd_drift(milFalcon, universe):
   print("TODO : DIRFT COMMAND")

def cmd_harvest(milFalcon, universe):
   currentPlanet = milFalcon.currPlanet
   if (bool(universe[currentPlanet].resources)):
      if (random.randint(0, 99) in range(0, 69)):
         print("SUCCESSFUL HARVEST!")
         for key, value in universe[currentPlanet].resources.items():
            if (key not in milFalcon.resources):
               milFalcon.resources.update({key:1})
            else:
               milFalcon.resources.update({key:(milFalcon.resources[key]+1)})
      else:
         print("UNSUCCESSFUL HARVEST..")
         
   universe[currentPlanet].resources = None

   milFalcon.fuel = milFalcon.fuel - 5

def cmd_trade(milFalcon, universe):
   currentPlanet = milFalcon.currPlanet
   print("TODO : TRADE COMMAND")

def cmd_fight(milFalcon, universe):
   currentPlanet = milFalcon.currPlanet
   civ = universe[currentPlanet].civ
   civHealth = universe[currentPlanet].civHealth
   print("Bandit Camp :", civHealth,"\n")
   
   if (civ == "Bandit"):
      userAttack = random.randint(milFalcon.damageMin, milFalcon.damageMax)
      banditAttack = random.randint(1, 4)
      milFalcon.health = milFalcon.health - banditAttack
      universe[currentPlanet].civHealth = universe[currentPlanet].civHealth - userAttack
      
      print(" User attacked for", userAttack, "damage.\n", civ, "dealed", banditAttack,"damage.")

   if (universe[currentPlanet].civHealth < 0):
      universe[currentPlanet].civ = None
      universe[currentPlanet].civHealth = None
      print("\nCivilization was defeated!")

def quitGame(milFalcon, universe) :
   sys.exit(0)

def updateStatus(milFalcon, universe) :
   currentPlanet = milFalcon.currPlanet
   print(
      "\n================================================================\n"
      "Ship Stats :\n",
      "Health :", milFalcon.health, "| Fuel :", milFalcon.fuel, "| Current Planet :", milFalcon.currPlanet,"\n",
      "Resources :", milFalcon.resources,"\n",
      "Damage Range :", milFalcon.damageMin,"-",milFalcon.damageMax,"\n",
      "Adjacent Planets :", universe[currentPlanet].adjPlanets, "\n\n"
      "Planet Stats :\n",
      "Planet Number : ", universe[currentPlanet].planetNum, "| Planet Type : ", universe[currentPlanet].planetType,"\n",
      "Planet Resources :", universe[currentPlanet].resources,"\n",
      "Civilization :", universe[currentPlanet].civ, "| Civ's Health :", universe[currentPlanet].civHealth,
      "\n================================================================\n")

def startGame (milFalcon, universe):
   commandList = {"goto":cmd_goto, "drift":cmd_drift,"harvest":cmd_harvest,
                  "trade":cmd_trade, "fight":cmd_fight, "q":quitGame}
   
   print("Welcome to [INSERT GAME NAME]!")
   updateStatus(milFalcon, universe)

   while (True):
      if (universe[milFalcon.currPlanet].planetType == "HOME"):
         print("Congratulations! You made it back home!")
         break
      
      userInput = input("$ ")

      if (userInput.split()[0] in commandList):
         if (userInput.split()[0] == "goto"):
            cmd_goto(int(userInput.split()[1]), milFalcon, universe)
         else:
            commandList[userInput.split()[0]](milFalcon, universe)

      updateStatus(milFalcon, universe)

   return 0
      
def main ():
   milFalcon, universe = generateMap()

   startGame(milFalcon, universe)
   
   return 0


if __name__ == '__main__': main()
