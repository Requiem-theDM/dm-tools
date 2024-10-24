#!/usr/bin/env python3

import os

def readPlayers():
    players = {}
    absentPlayers = []
    with open(f"../savedData/players.tsv","r") as file:
        file.readline()
        for line in file:
            fields = line.rstrip("\n").split("\t")
            players.setdefault(fields[0],int(fields[1]))
    for player in players.keys():
        present = input(f"Is {player} present? ")
        if present.lower() == "all":
            print(f"## All players marked present.")
            return players
        elif present.lower() in ["n","no"]:
            absentPlayers.append(player)
        elif present.lower() in ["y","yes"]:
            continue
    for player in absentPlayers:
        del players[player]
    print(f"## Your current players are as follows:")
    for player in players.keys():
        print(f"## {player}")
    return players

def checkPlayerFile():
    if os.path.exists("../savedData/players.tsv"):
        return
    else:
        players = {}
        numPlayers = int(input("How many players do you have? "))
        for i in range(numPlayers):
            player = input(f"What is player {i + 1}'s name? ")
            level = int(input(f"What is {player}'s level? "))
            if level < 1: level = 1
            if level > 10: level = 10
            players.setdefault(player,level)
        with open(f"../savedData/players.tsv","w") as file:
            file.write(f"Player\tLevel\n")
            for player, level in players.items():
                file.write(f"{player}\t{level}\n")

def modeSelector():
    checkPlayerFile()
    mode = input(f"Please select the player management you would like to perform.\n## Level Up: Increase character level with l, level, levelup, level_up, or level up.\n## Add a Player: Add a player to the current list of players with a or add.\n## Remove a Player: Remove a player from the current list of players with r, rem, or remove.\n## Cancel Player Management with c, can, or cancel.\nPlease enter your selection: ")
    if mode.lower() in ["l","a","r","level","levelup","level_up","level up","add","rem","remove","c","can","cancel"]:
        return mode
    else:
        print(f"Invalid Mode: \"{mode}\" was selected. Please choose a valid mode.")
        modeSelector()

def levelUp():
    players = {}
    with open(f"../savedData/players.tsv","r") as file:
        file.readline()
        for line in file:
            fields = line.rstrip("\n").split("\t")
            players.setdefault(fields[0],int(fields[1]))
    print(f"## Your current players are as follows:")
    for player in players.keys():
        print(f"## {player}")
    levelup = input(f"Which player would you like to level up? ")
    if levelup in players.keys():
        level = int(input(f"What is {levelup}'s new level? "))
        if level < 1: level = 1
        if level > 10: level = 10
        players[levelup] = level
        with open(f"../savedData/players.tsv","w") as file:
            file.write(f"Player\tLevel\n")
            for player, level in players.items():
                file.write(f"{player}\t{level}\n")
    else:
        print(f"Player: \"{levelup}\" was not found. Please select a valid player.")
        levelUp()
    exitState = input(f"Continue Leveling Up?\nYes or No: ")
    if exitState.lower() in ["y","yes"]:
        levelUp()
    elif exitState.lower() in ["n","no"]:
        return
    else:
        print(f"Invalid Response Received: \"{exitState}\"")
        return

def addPlayer():
    players = {}
    with open(f"../savedData/players.tsv","r") as file:
        file.readline()
        for line in file:
            fields = line.rstrip("\n").split("\t")
            players.setdefault(fields[0],int(fields[1]))
    newPlayer = input(f"What is the new player's name? ")
    level = int(input(f"What is {newPlayer}'s level? "))
    if level < 1: level = 1
    if level > 10: level = 10
    players.setdefault(newPlayer,level)
    with open(f"../savedData/players.tsv","w") as file:
            file.write(f"Player\tLevel\n")
            for player, level in players.items():
                file.write(f"{player}\t{level}\n")
    exitState = input(f"Continue Adding Players?\nYes or No: ")
    if exitState.lower() in ["y","yes"]:
        addPlayer()
    elif exitState.lower() in ["n","no"]:
        return
    else:
        print(f"Invalid Response Received: \"{exitState}\"")
        return

def removePlayer():
    players = {}
    with open(f"../savedData/players.tsv","r") as file:
        file.readline()
        for line in file:
            fields = line.rstrip("\n").split("\t")
            players.setdefault(fields[0],int(fields[1]))
    print(f"## Your current players are as follows:")
    for player in players.keys():
        print(f"## {player}")
    remove = input(f"Which player would you like to remove? ")
    if remove in players.keys():
        del players[remove]
        with open(f"../savedData/players.tsv","w") as file:
            file.write(f"Player\tLevel\n")
            for player, level in players.items():
                file.write(f"{player}\t{level}\n")
    else:
        print(f"Player: \"{remove}\" was not found. Please select a valid player.")
        removePlayer()
    exitState = input(f"Continue Removing Players?\nYes or No: ")
    if exitState.lower() in ["y","yes"]:
        removePlayer()
    elif exitState.lower() in ["n","no"]:
        return
    else:
        print(f"Invalid Response Received: \"{exitState}\"")
        return

def managePlayers(mode):
    if mode.lower() in ["l","level","levelup","level_up","level up"]:
        levelUp()
    if mode.lower() in ["a","add"]:
        addPlayer()
    if mode.lower() in ["r","rem","remove"]:
        removePlayer()

def exitPrompt():
    exitState = input(f"Continue Player Management?\nYes or No: ")
    if exitState.lower() in ["y","yes"]:
        playerManager()
    elif exitState.lower() in ["n","no"]:
        return
    else:
        print(f"Invalid Response Received: \"{exitState}\"")
        exitPrompt()

def playerManager():
    mode = modeSelector()
    if mode in ["c","can","cancel"]: return
    else:
        managePlayers(mode)
        exitPrompt()