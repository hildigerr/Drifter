#!/usr/bin/python
################################################################################
#                                                                              #
# Crafting.py -- The Spaceship                                                 #
#                                                                              #
#   Western Washington University -- CSCI 4/597H -- Spring 2016                #
#                                                                              #
################################################################################

import random

## Dictionary of requirements to craft the item. ##
CRAFT_FUEL = {"Plasma":4, "Laser":6, "Holy Water":8}
CRAFT_PLASMA = {"Charcoal":8, "Holy Water":8, "Obsidian":8}
CRAFT_LASER = {"Metal":5, "Stones":4, "Lava":2, "Charcoal":5}
CRAFT_CARGO = {"Metal":15, "Stones":7, "Lava":3, "Water":6, "Gems":5}

## Dictionary to map the requirements to the item. ##
CRAFT_LIST = {"Laser":CRAFT_LASER, "Cargo":CRAFT_CARGO, "Plasma":CRAFT_PLASMA, "Fuel":CRAFT_FUEL}

########################################################################## Craft:
class Craft():
   def craft(ship, inv, item, amt):
      req = CRAFT_LIST.get(item)
      print("You want to craft", amt, item + "(s).");

      for key in req:
           if (key not in inv) or ((req[key] * amt) > inv[key]):
              print("You do not have the required resources to craft", item + ".\n");
              return False

      for key in req:
         inv[key] -= (req[key] * amt)
         if inv[key] == 0:
            inv.pop(key)

      if (item == "Cargo"):
         ship.cap += 25 * amt
      if (item == "Fuel"):
         ship.fuel += 10 * amt
      else:
         if item not in inv:
            ship.cargo.update({item:amt});
         else:
            ship.cargo.update({item:inv[item]+amt});
      print("You crafted", amt, item + "(s)!\n");
      return True

if __name__ == '__main__':
   crafting = Craft()

