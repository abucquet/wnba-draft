import numpy as np
from collections import defaultdict

NUM_IN_CONFERENCE_GAMES = 4
NUM_OUT_CONFERENCE_GAMES = 3

WNBA_TEAMS = [
    "Dream","Sky","Sun","Fever","Mystics","Wings","Aces","Sparks","Lynx","Mercury","Storm"
]
east = ["Dream","Sky","Sun","Fever","Liberty","Mystics"]
west = ["Wings","Aces","Sparks","Lynx","Mercury","Storm"]
elo = {
    "Wings":1463,
    "Liberty":1432,
    "Sparks":1507,
    "Sun":1601,
    "Dream":1469,
    "Sky":1457,
    "Fever":1368,
    "Mystics":1469,
    "Aces":1601,
    "Lynx":1487,
    "Mercury":1516,
    "Storm":1630
    }

tankCoef = 0.9

def simulateMatch(teamA, teamB, tankA, tankB, teamRecords, gamesPlayed, teamWinLoss):
    #Given teams A and B and whether or not each is tanking, choose a winner from the 2:
    eloA = elo[teamA]
    eloB = elo[teamB]
    if tankA:
        eloA*= tankCoef
    if tankB:
        eloB *= tankCoef
    probA = 1/(1 + 10**((eloB - eloA)/400)) # eloA/(eloA+eloB)
    if np.random.rand() < probA:
        teamRecords[teamA] += 1
        teamWinLoss[teamA].append(1)
        teamWinLoss[teamB].append(0)
    else:
        teamRecords[teamB] += 1
        teamWinLoss[teamA].append(1)
        teamWinLoss[teamB].append(0)
    gamesPlayed[teamA] += 1
    gamesPlayed[teamB] += 1

    return teamRecords, gamesPlayed, teamWinLoss

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
    teamRecords = defaultdict(int) # map teams to wins
    gamesPlayed = defaultdict(int) # map teams to games played
    teamWinLoss = defaultdict(list) # map teams to win loss outcomes (list of 0s and 1s)

    games = createGames()
    for game in games:
        teamRecords, gamesPlayed, teamWinLoss = simulateMatch(
            game[0], game[1], False, False,
            teamRecords, gamesPlayed, teamWinLoss
            )

    return teamRecords, gamesPlayed, teamWinLoss
    
# simulateSeason()
