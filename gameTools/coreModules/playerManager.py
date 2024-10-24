#!/usr/bin/env python3

import os

def readPlayers():
    checkPlayerFile()
    players = {}
    absentPlayers = []
    with open(f"../savedData/players.tsv","r") as file:
        file.readline()
        for line in file:
            fields = line.rstrip("\n").split("\t")
            players.setdefault(fields[0],int(fields[1]))
    for player in players.keys():
        while True:
            try:
                present = input(f"Is {player} present? ")
                assert present.lower() in ["y","n","yes","no","all"]
                break
            except:
                print(f"Invalid Response Received: \"{present}\" Please Enter Yes or No, or Enter All to Mark All Players Present.")
        if present.lower() == "all":
            print(f"## All players marked present.")
            return players
        elif present.lower() in ["n","no"]:
            absentPlayers.append(player)
        else:
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
        while True:
            try:
                numPlayers = int(input("How many players do you have? "))
                assert numPlayers < 0
                break
            except:
                print(f"Invalid Response Received: \"{numPlayers}\" Please Enter A Positive Number.")
        for i in range(numPlayers):
            while True:
                try:
                    player = input(f"What is player {i + 1}'s name? ")
                    if player == "": raise ValueError
                    break
                except:
                    print(f"No player name was entered. Please Enter A Player Name.")
            while True:
                try:
                    level = int(input(f"What is {player}'s level? "))
                    assert 0 < level < 11
                    break
                except:
                    print(f"Invalid Response Received: \"{level}\" Please Enter An Integer Between 1 and 10.")
            players.setdefault(player,level)
        with open(f"../savedData/players.tsv","w") as file:
            file.write(f"Player\tLevel\n")
            for player, level in players.items():
                file.write(f"{player}\t{level}\n")

def modeSelector():
    checkPlayerFile()
    while True:
        try:
            mode = input(f"Please select the player management you would like to perform.\n## Level Up: Increase character level with l, level, levelup, level_up, or level up.\n## Add a Player: Add a player to the current list of players with a or add.\n## Remove a Player: Remove a player from the current list of players with r, rem, or remove.\n## Cancel Player Management with c, can, or cancel.\nPlease enter your selection: ")
            assert mode.lower() in ["l","a","r","level","levelup","level_up","level up","add","rem","remove","c","can","cancel"]
            break
        except:
            print(f"Invalid Mode: \"{mode}\" was selected. Please choose a valid mode.")
    return mode

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
    while True:
        try:
            levelup = input(f"What is player {i + 1}'s name? ")
            if levelup == "": raise ValueError
            break
        except:
            print(f"No player name was entered. Please Enter A Player Name.")
    if levelup in players.keys():
        while True:
            try:
                level = int(input(f"What is {player}'s level? "))
                assert 0 < level < 11
                break
            except:
                print(f"Invalid Response Received: \"{level}\" Please Enter An Integer Between 1 and 10.")
        players[levelup] = level
        with open(f"../savedData/players.tsv","w") as file:
            file.write(f"Player\tLevel\n")
            for player, level in players.items():
                file.write(f"{player}\t{level}\n")
    else:
        print(f"Player: \"{levelup}\" was not found. Please select a valid player.")
        levelUp()
    while True:
        try:
            exitState = input(f"Continue Leveling Up?\nYes or No: ")
            assert exitState.lower() in ["y","n","yes","no"]
            break
        except:
            print(f"Invalid Response Received: \"{exitState}\" Please Enter Yes or No.")
    if exitState.lower() in ["y","yes"]:
        levelUp()
    else:
        return

def addPlayer():
    players = {}
    with open(f"../savedData/players.tsv","r") as file:
        file.readline()
        for line in file:
            fields = line.rstrip("\n").split("\t")
            players.setdefault(fields[0],int(fields[1]))
    while True:
        try:
            newPlayer = input(f"What is player {i + 1}'s name? ")
            if newPlayer == "": raise ValueError
            break
        except:
            print(f"No player name was entered. Please Enter A Player Name.")
    while True:
            try:
                level = int(input(f"What is {newPlayer}'s level? "))
                assert 0 < level < 11
                break
            except:
                print(f"Invalid Response Received: \"{level}\" Please Enter An Integer Between 1 and 10.")
    players.setdefault(newPlayer,level)
    with open(f"../savedData/players.tsv","w") as file:
            file.write(f"Player\tLevel\n")
            for player, level in players.items():
                file.write(f"{player}\t{level}\n")
    while True:
        try:
            exitState = input(f"Continue Adding Players?\nYes or No: ")
            assert exitState.lower() in ["y","n","yes","no"]
            break
        except:
            print(f"Invalid Response Received: \"{exitState}\" Please Enter Yes or No.")
    if exitState.lower() in ["y","yes"]:
        addPlayer()
    else:
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
    while True:
        try:
            remove = input(f"Which player would you like to remove? ")
            assert remove in players.keys()
            break
        except:
            print(f"Player: \"{remove}\" was not found. Please select a valid player.")
    del players[remove]
    with open(f"../savedData/players.tsv","w") as file:
        file.write(f"Player\tLevel\n")
        for player, level in players.items():
            file.write(f"{player}\t{level}\n")
    while True:
        try:
            exitState = input(f"Continue Removing Players?\nYes or No: ")
            assert exitState.lower() in ["y","n","yes","no"]
            break
        except:
            print(f"Invalid Response Received: \"{exitState}\" Please Enter Yes or No.")
    if exitState.lower() in ["y","yes"]:
        removePlayer()
    else:
        return

def managePlayers(mode):
    if mode.lower() in ["l","level","levelup","level_up","level up"]:
        levelUp()
    if mode.lower() in ["a","add"]:
        addPlayer()
    if mode.lower() in ["r","rem","remove"]:
        removePlayer()

def exitPrompt():
    while True:
        try:
            exitState = input(f"Continue Player Management?\nYes or No: ")
            assert exitState.lower() in ["y","n","yes","no"]
            break
        except:
            print(f"Invalid Response Received: \"{exitState}\" Please Enter Yes or No.")
    if exitState.lower() in ["y","yes"]:
        playerManager()
    else:
        return

def playerManager():
    mode = modeSelector()
    if mode in ["c","can","cancel"]: return
    else:
        managePlayers(mode)
        exitPrompt()