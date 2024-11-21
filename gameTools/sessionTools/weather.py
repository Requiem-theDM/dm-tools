#!/usr/bin/env python3
import argparse as ap
import pandas as pd
from ast import literal_eval
import numpy as np

def parseargs():
    parser = ap.ArgumentParser(description='Generates Weather Appropriate to a Given Season')
    parser.add_argument('season',type=str,help="Sets the season to pull weather data for.")
    parser.add_argument('-c', '--changes',default=1,type=int,help='If present, changes weather the selected number of times.')
    parser.add_argument('-s', '--set',type=int,choices=range(0,19),metavar="[0-18]", help='If present, sets the weather state for the selected season to the specified value (0-18).')
    parser.add_argument('-v', '--validation',action='store_true',help='If present, runs the matrix checker on the transition matrix for the selected season, then exits.')
    args = parser.parse_args()
    return args

# default_transition_matrix = np.array([
#         [7/36, 2/36, 2/36, 5/36, 6/36, 9/36, 5/36, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Hex 1 can transition to 1, 2, 3, 4, 5, 6, and 7
#         [6/36, 7/36, 5/36, 0, 0, 0, 9/36, 5/36, 2/36, 2/36, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Hex 2 can transition to 2, 9, 10, 3, 1, 7, and 8
#         [9/36, 5/36, 7/36, 6/36, 0, 0, 0, 0, 0, 2/36, 2/36, 5/36, 0, 0, 0, 0, 0, 0, 0], # Hex 3 can transition to 3, 10, 11, 12, 4, 1, and 2
#         [5/36, 0, 2/36, 7/36, 9/36, 0, 0, 0, 0, 0, 0, 2/36, 5/36, 6/36, 0, 0, 0, 0, 0], # Hex 4 can transition to 4, 3, 12, 13, 14, 5, and 1
#         [2/36, 0, 0, 2/36, 7/36, 5/36, 0, 0, 0, 0, 0, 0, 0, 5/36, 6/36, 9/36, 0, 0, 0], # Hex 5 can transition to 5, 1, 4, 14, 15, 16, and 6
#         [2/36, 0, 0, 0, 5/36, 7/36, 2/36, 0, 0, 0, 0, 0, 0, 0, 0, 6/36, 9/36, 5/36, 0], # Hex 6 can transition to 6, 7, 1, 5, 16, 17, and 18 
#         [5/36, 2/36, 0, 0, 0, 6/36, 7/36, 2/36, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9/36, 5/36], # Hex 7 can transition to 7, 8, 2, 1, 6, 18, and 19
#         [0, 5/36, 0, 0, 0, 0, 6/36, 7/36, 2/36, 0, 0, 5/36, 0, 0, 0, 2/36, 0, 0, 9/36], # Hex 8 can transition to 8, 16, 9, 2, 7, 19, and 12
#         [0, 6/36, 0, 0, 0, 0, 0, 9/36, 7/36, 5/36, 5/36, 0, 0, 0, 2/36, 0, 0, 0, 2/36], # Hex 9 can transition to 9, 15, 19, 10, 2, 8, and 11
#         [0, 9/36, 6/36, 0, 0, 0, 0, 0, 5/36, 7/36, 5/36, 0, 0, 0, 2/36, 0, 0, 2/36, 0], # Hex 10 can transition to 10, 15, 18, 11, 3, 2, and 9.
#         [0, 0, 9/36, 0, 0, 0, 0, 0, 5/36, 5/36, 7/36, 6/36, 2/36, 0, 0, 0, 2/36, 0, 0], # Hex 11 can transition to 11, 13, 17, 9, 12, 3, and 10.
#         [0, 0, 5/36, 9/36, 0, 0, 0, 5/36, 0, 0, 2/36, 7/36, 6/36, 0, 0, 2/36, 0, 0, 0], # Hex 12 can transition to 12, 11, 16, 8, 13, 4, and 3
#         [0, 0, 0, 5/36, 0, 0, 0, 0, 0, 0, 6/36, 2/36, 7/36, 9/36, 2/36, 0, 0, 0, 5/36], # Hex 13 can transition to 13, 12, 15, 19, 11, 14, and 4
#         [0, 0, 0, 2/36, 5/36, 0, 0, 0, 0, 6/36, 0, 0, 2/36, 7/36, 9/36, 0, 0, 5/36, 0], # Hex 14 can transition to 14, 4, 13, 18, 10, 15, and 5
#         [0, 0, 0, 0, 2/36, 0, 0, 0, 6/36, 0, 0, 0, 9/36, 2/36, 7/36, 5/36, 5/36, 0, 0], # Hex 15 can transition to 15, 5, 14, 17, 9, 13, and 16
#         [0, 0, 0, 0, 2/36, 2/36, 0, 6/36, 0, 0, 0, 9/36, 0, 0, 5/36, 7/36, 5/36, 0, 0], # Hex 16 can transition to 16, 6, 5, 15, 8, 12, and 17
#         [0, 0, 0, 0, 0, 2/36, 0, 0, 0, 0, 9/36, 0, 0, 0, 5/36, 5/36, 7/36, 2/36, 6/36], # Hex 17 can transition to 17, 18, 6, 16, 19, 11, and 15
#         [0, 0, 0, 0, 0, 5/36, 2/36, 0, 0, 9/36, 0, 0, 0, 5/36, 0, 0, 6/36, 7/36, 2/36], # Hex 18 can transition to 18, 19, 7, 6, 17, 10, and 14
#         [0, 0, 0, 0, 0, 0, 5/36, 2/36, 9/36, 0, 0, 0, 5/36, 0, 0, 0, 2/36, 6/36, 7/36] # Hex 19 can transition to 19, 17, 8, 7, 18, 9, and 13
#     ])

def addWall(matrix,hex1,hex2):
    matrix[hex1,hex1] += matrix[hex1,hex2]
    matrix[hex1,hex2] = 0
    matrix[hex2,hex2] += matrix [hex2,hex1]
    matrix[hex2,hex1] = 0
    return matrix

def matrixChecker(season,seasonData,weatherChanges):
    import matplotlib.pyplot as plt
    seasonMatrix = np.loadtxt("../../savedData/default_transition_matix.csv",delimiter=',')
    for wall in seasonData.loc[seasonData.Season == season, 'Walls'].iloc[0]:
        seasonMatrix = addWall(seasonMatrix,wall[0],wall[1])
    for hex in range(seasonMatrix.shape[0]):
        print(f"The transition probability sum for {seasonData.loc[seasonData.Season == season, 'States'].iloc[0][hex]} is {format(np.sum(seasonMatrix[hex])*100,'.0f')}%.")
        for position, transition in enumerate(seasonMatrix[hex]):
            if transition != 0: print(f"The transition probability to {seasonData.loc[seasonData.Season == season, 'States'].iloc[0][position]} is {format(transition * 36,'.0f')}/36")
        print()
        if np.sum(seasonMatrix[hex]) > 1:
           raise Exception(f"The transition probability sum for hex {hex + 1} exceeds 100%!")
    startingState = [0] * seasonMatrix.shape[0]
    startingState[seasonData.loc[seasonData.Season == season, 'State'].iloc[0]] = 1
    plt.bar(range(19),np.dot(startingState,np.linalg.matrix_power(seasonMatrix,weatherChanges)))
    plt.ylabel("Probability")
    plt.xlabel("Ending Weather")
    plt.title(f"Probability Distributon of {season.capitalize()} Ending Weather After {weatherChanges} Change{'s' if weatherChanges != 1 else ''}, Starting at {seasonData.loc[seasonData.Season == season, 'States'].iloc[0][seasonData.loc[seasonData.Season == season, 'State'].iloc[0]]}")
    plt.xticks(range(19),(seasonData.loc[seasonData.Season == season, 'States'].iloc[0]),rotation=45, ha='right')
    plt.subplots_adjust(bottom=.2)
    plt.show()
    exit()

def spiceDrawer():
    seasonData = pd.read_csv(f"../../savedData/weather.csv",delimiter=",",index_col=False,converters={'States': literal_eval,'Walls': literal_eval})
    return seasonData

def changeWeather(season,seasonData,weatherChanges):
    seasonMatrix = np.loadtxt("../../savedData/default_transition_matix.csv",delimiter=',')
    for wall in seasonData.loc[seasonData.Season == season, 'Walls'].iloc[0]:
        seasonMatrix = addWall(seasonMatrix,wall[0],wall[1])
    startingState = [0] * seasonMatrix.shape[0]
    startingState[seasonData.loc[seasonData.Season == season, 'State'].iloc[0]] = 1
    seasonData.loc[seasonData.Season == season, 'State'] = np.random.choice(range(seasonMatrix.shape[0]),p=(np.dot(startingState,np.linalg.matrix_power(seasonMatrix,weatherChanges))))
    return seasonData

def saveSeason(seasonData):
    seasonData.to_csv("../../savedData/weather.csv",sep=",",mode="w",header=True,index=False)

def main():
    args = parseargs()
    seasonData = spiceDrawer()
    if seasonData['Season'].isin([args.season]).any() == False:
        print(f"No data for {args.season} was found.")
        print(f"You have data for the following seasons:",end=" ")
        print(*seasonData['Season'])
        exit()
    if args.set in range(19):
        print(f"Setting Weather Pattern")
        seasonData.loc[seasonData.Season == args.season, 'State'] = args.set
    if args.validation == True:
        matrixChecker(args.season,seasonData,args.changes)
    print(f"The current weather is: {seasonData.loc[seasonData.Season == args.season, 'States'].iloc[0][seasonData.loc[seasonData.Season == args.season, 'State'].iloc[0]]}.")
    if args.set in range(19) and args.changes != 1 or not(args.set):
        print(f"Changing Weather Pattern")
        changeWeather(args.season,seasonData,args.changes)
    print(f"The new weather is: {seasonData.loc[seasonData.Season == args.season, 'States'].iloc[0][seasonData.loc[seasonData.Season == args.season, 'State'].iloc[0]]}.")
    saveSeason(seasonData)

if __name__ == "__main__":
    main()