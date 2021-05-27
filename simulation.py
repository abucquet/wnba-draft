import numpy as np
from collections import defaultdict

NUM_IN_CONFERENCE_GAMES = 4
NUM_OUT_CONFERENCE_GAMES = 3

teams = ["Dream","Sky","Sun","Fever","Mystics","Wings","Aces","Sparks","Lynx","Mercury","Storm"]
east = ["Dream","Sky","Sun","Fever","Liberty","Mystics"]
west = ["Wings","Aces","Sparks","Lynx","Mercury","Storm"]
elo = {"Wings":1100,"Liberty":1058,"Sparks":954,"Sun":1067,"Dream":950,
        "Sky":860,"Fever":940,"Mystics":1042,"Aces":1120,"Lynx":912,"Mercury":1029,"Storm":987}

tankCoef = 0.8
teamRecords = defaultdict(int) #map teams to wins
gamesPlayed = defaultdict(int) #map teams to games played

def simulateMatch(teamA,teamB,tankA,tankB):
    #Given teams A and B and whether or not each is tanking, choose a winner from the 2:
    eloA = elo[teamA]
    eloB = elo[teamB]
    if tankA:
        eloA*= tankCoef
    if tankB:
        eloB *= tankCoef
    probA = eloA/(eloA+eloB)
    if np.random.rand() < probA:
        teamRecords[teamA] += 1
    else:
        teamRecords[teamB] += 1
    gamesPlayed[teamA] += 1
    gamesPlayed[teamB] += 1

def createGames():
    pairings = []
    for eastInd in range(len(east)):
        for oppInd in range(eastInd+1,len(east)):
            for _ in range(NUM_IN_CONFERENCE_GAMES):
                pairings.append((east[eastInd],east[oppInd]))
        for oppInd in range(len(west)):
            for _ in range(NUM_OUT_CONFERENCE_GAMES):
                pairings.append((east[eastInd],west[oppInd]))

    for westInd in range(len(west)):
        for oppInd in range(westInd+1,len(west)):
            for _ in range(NUM_IN_CONFERENCE_GAMES):
                pairings.append((west[westInd],west[oppInd]))

    return pairings

def simulateSeason():
    games = createGames()
    for game in games:
        simulateMatch(game[0],game[1],False,False)
    print(teamRecords)
    print(gamesPlayed)

simulateSeason()
