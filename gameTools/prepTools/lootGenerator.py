#!/usr/bin/env python3

import argparse as ap
import numpy as np

def parseargs():
    parser = ap.ArgumentParser(description='Generates Level Appropriate Loot for a Dungeon')
    parser.add_argument('playerCount',type=int,help="Sets the number of players the dungeon is designed for.")
    parser.add_argument('averageLevel',type=int,help="Sets the average player level the dungeon is designed for.")
    parser.add_argument('dungeonSize',type=int,help="Sets the maximum number of rooms in the dungeon.")
    parser.add_argument('-d', '--difficulty',default=1.0,type=float,help='If present, multiplies the treasure reward by the provided difficulty modifier.')
    args = parser.parse_args()
    return args

def generateTreasure(playerCount,averageLevel,dungeonSize,difficulty):
    lootByLevel = {1:200,2:200,3:300,4:300,5:400,6:400,7:400,8:400,9:400,10:400}
    if difficulty == 1:
        print(f"## Generating Loot for {playerCount} players of average level: {averageLevel}.")
    else:
        print(f"## Generating Loot for {playerCount} players of average level: {averageLevel} with a difficulty modifier of {difficulty}.")
    totalTreasure = float(lootByLevel[averageLevel] * playerCount * difficulty * (1 + 0.1 * (np.random.random() - 0.5)))
    print(f"## Treasure Number\tTreasure Value")
    for room in range(dungeonSize):
        roomTreasure = float(format(totalTreasure * (0.5 ** (room + 1)),'.2f'))
        if roomTreasure > 0 and roomTreasure > 1:
            print(f"## Treasure {room + 1}\t{roomTreasure} SP")
        if roomTreasure > 0 and roomTreasure < 1:
            print(f"## Treasure {room + 1}\t{float(format(roomTreasure * 100,'.2f'))} CP")

def main():
    args = parseargs()
    generateTreasure(args.playerCount,args.averageLevel,args.dungeonSize,args.difficulty)
    
if __name__ == "__main__":
    main()