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
DONE - goto
drift - no one votes, default action
head home

in planet :
DONE - harvest - has resources
trade - has civ
DONE - fight - has civ
leave - system

========================================
'''

# Classes for an 'object' for the ship and planets.
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

# Generate resources on a planet randomly based on the
# planet type.
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

# Generate a 10x10 matrix with all nodes connected to create the
# universe. Planets has resources and possible civilization.
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
            planet.civStatus = "Hostile"
         else:
            planet.civHealth = 70
            planet.civStatus = "Passive"
         
      universe.append(planet)

   homePlanet = universe[random.randint(0, 9)]
   homePlanet.planetType = "HOME"

   startPlanet = universe[random.randint(90, 99)]
   startPlanet.planetType = "STRT"

   milFalcon = makeMilFalcon()
   milFalcon.currPlanet = startPlanet.planetNum

   return (milFalcon, universe)

# Ship goes to the next planet adjacent to the current planet.
def cmd_goto(gotoPlanet, milFalcon, universe):
   currentPlanet = milFalcon.currPlanet
   adjPlanets = universe[currentPlanet].adjPlanets

   if (universe[currentPlanet].civStatus == "Hostile"):
      banditAttack (milFalcon, universe)

   if (gotoPlanet in adjPlanets):
      print("- Travelling to Planet #", gotoPlanet, "...")
      milFalcon.currPlanet = gotoPlanet
      milFalcon.fuel = milFalcon.fuel - 10
   else:
      print("ERROR : Planet #", gotoPlanet, "is not adjacent.")
   return 0

def cmd_drift(milFalcon, universe):
   print("TODO : DIRFT COMMAND")
   return 0

# Harvest resources on the planet, if planet has bandits they
# have a chance to attack the ship. 70% chance success.
def cmd_harvest(milFalcon, universe):
   currentPlanet = milFalcon.currPlanet

   if (universe[currentPlanet].civStatus == "Hostile"):
      banditAttack (milFalcon, universe)
   
   if (bool(universe[currentPlanet].resources)):
      if (random.randint(0, 99) in range(0, 69)):
         print("- SUCCESSFUL HARVEST!")
         for key, value in universe[currentPlanet].resources.items():
            if (key not in milFalcon.resources):
               milFalcon.resources.update({key:1})
            else:
               milFalcon.resources.update({key:(milFalcon.resources[key]+1)})
      else:
         print("- UNSUCCESSFUL HARVEST..")
   else:
      print("- There are no resources left on this planet.")
         
   universe[currentPlanet].resources = None
   milFalcon.fuel = milFalcon.fuel - 5
   return 0

# Trade with the civilization that the ship is on.
def cmd_trade(milFalcon, universe):
   currentPlanet = milFalcon.currPlanet
   
   if (universe[currentPlanet].civ == "Trading") :
      print("\n- Trading Prices\n")
   else:
      print("- No civilization to trade with.")
   return 0

# Fights the civilization on the planet, the civilization status will
# change to 'Hostile' when attacked.
def cmd_fight(milFalcon, universe):
   currentPlanet = milFalcon.currPlanet
   civ = universe[currentPlanet].civ
   civHealth = universe[currentPlanet].civHealth
   
   if (civ == "Bandit"):
      print("Bandit Camp :", civHealth, "[", universe[currentPlanet].civStatus,"]\n")
   elif (civ == "Trading"):
      universe[currentPlanet].civStatus = "Hostile"
      print("Trading Camp :", civHealth, "[", universe[currentPlanet].civStatus,"]\n")
      
   userAttack = random.randint(milFalcon.damageMin, milFalcon.damageMax)
   civAttack = random.randint(1, 4)
   milFalcon.health = milFalcon.health - civAttack
   universe[currentPlanet].civHealth = universe[currentPlanet].civHealth - userAttack
      
   print("- User attacked for", userAttack, "damage.\n", civ, "dealed", civAttack,"damage.")

   if (universe[currentPlanet].civHealth < 0):
      universe[currentPlanet].civ = None
      universe[currentPlanet].civHealth = None
      print("\nCivilization was defeated!")
      
   return 0

# Bandits attack ship if they perform an action on a planet with bandits.
# 70% chance of attacking.
def banditAttack (milFalcon, universe):
   if (random.randint(0, 99) in range(0, 69)):
      civAttack = random.randint(1, 4)
      milFalcon.health = milFalcon.health - civAttack
      print("- Bandits dealed", civAttack, "damage.")
   
   return 0

# Quit the game.
def quitGame(milFalcon, universe) :
   sys.exit(0)

# Update the status of the game
def updateStatus(milFalcon, universe) :
   currentPlanet = milFalcon.currPlanet
   print(
      "\n============================== BEGIN ============================\n"
      "Ship Stats :\n",
      "Health :", milFalcon.health, "| Fuel :", milFalcon.fuel, "| Current Planet :", milFalcon.currPlanet,"\n",
      "Resources :", milFalcon.resources,"\n",
      "Damage Range :", milFalcon.damageMin,"-",milFalcon.damageMax,"\n",
      "Adjacent Planets :", universe[currentPlanet].adjPlanets, "\n\n"
      "Planet Stats :\n",
      "Planet Number : ", universe[currentPlanet].planetNum, "| Planet Type : ", universe[currentPlanet].planetType,"\n",
      "Planet Resources :", universe[currentPlanet].resources,"\n",
      "Civilization :", universe[currentPlanet].civ, "[", universe[currentPlanet].civStatus,"] | Civ's Health :", universe[currentPlanet].civHealth,
      "\n============================== END ==============================\n")
   return 0

# Run function corresponding to user input.
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

# Main function to create the map and start the game.
def main ():
   milFalcon, universe = generateMap()
   startGame(milFalcon, universe)
   return 0


if __name__ == '__main__': main()
