#!/usr/bin/env python3

import os
import sys
import argparse as ap
import numpy as np
from gameTools.coreModules.playerManager import *

def parseargs():
    parser = ap.ArgumentParser(description='Generates Level Appropriate Loot for a Dungeon')
    parser.add_argument('-pm', '--playerManager',action='store_true',help='If present, activates the player manager.')
    parser.add_argument('-d', '--difficulty',default=1.0,help='Accepts user input for a multiplier of the total treasure reward based on difficulty.')
    args = parser.parse_args()
    return args

def generateTreasure(difficulty, players):
    lootByLevel = {}
    averageLevel = int(str(np.floor(sum(players.values())/len(players))).rstrip(".0"))
    if difficulty == 1:
        print(f"## Generating Loot for {len(players)} players of average level: {averageLevel}.")
    else:
        print(f"## Generating Loot for {len(players)} players of average level: {averageLevel} with a difficulty modifier of {difficulty}.")
    with open(f"../savedData/lootByLevel.tsv","r") as file:
        file.readline()
        for line in file:
            fields = line.rstrip("\n").split("\t")
            lootByLevel.setdefault(int(fields[0]),int(fields[1]))
    totalTreasure = float(lootByLevel[averageLevel] * len(players) * float(difficulty) * (1 + 0.1 * (np.random.random() - 0.5)))

    dungeonSize = int(input(f"How many rooms does this dungeon have? "))
    print(f"## Treasure Number\tTreasure Value")
    for room in range(dungeonSize):
        roomTreasure = float(format(totalTreasure * (0.5 ** (room + 1)),'.2f'))
        if roomTreasure > 0 and roomTreasure > 1:
            print(f"## Treasure {room + 1}\t{roomTreasure} SP")
        if roomTreasure > 0 and roomTreasure < 1:
            print(f"## Treasure {room + 1}\t{float(format(roomTreasure * 100,'.2f'))} CP")
    

def exitPrompt():
    exitState = input(f"Generate another dungeon?\nYes or No: ")
    if exitState.lower() in ["yes","y"]:
        newDifficulty = float(input(f"What difficulty level should the new dungeon be? "))
        main(1, newDifficulty)
    elif exitState.lower() in ["no","n"]:
        exit()
    else:
        print(f"Invalid Response Received: \"{exitState}\"")
        exitPrompt()

def main(startState=0, newDifficulty=1):
    args = parseargs()
    if startState == 0: os.chdir("../")
    elif startState != 0:
        args.difficulty = newDifficulty
        args.playerManager = False
    if args.playerManager == True:
        playerManager()
    players = readPlayers()
    generateTreasure(args.difficulty, players)
    exitPrompt()

if __name__ == "__main__":
    main()