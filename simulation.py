import numpy as np
from collections import defaultdict
import itertools as it
import matplotlib.pyplot as plt


NUM_IN_CONFERENCE_GAMES = 4
NUM_OUT_CONFERENCE_GAMES = 3
NUM_GAMES_PER_TEAM = NUM_IN_CONFERENCE_GAMES*5+NUM_OUT_CONFERENCE_GAMES*6

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

#FIX SHOULD BE 38 GAMES PER TEAM
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

def simulateSeason(games, tankingTeams=[],tankingStart=NUM_GAMES_PER_TEAM+1):
    teamRecords = defaultdict(int) # map teams to wins
    gamesPlayed = defaultdict(int) # map teams to games played
    teamWinLoss = defaultdict(list) # map teams to win loss outcomes (list of 0s and 1s)

    games = createGames()
    for game in games:
        A = game[0]
        B = game[1]
        tankA = False
        tankB = False
        # If record below certain threshold and percentage of games played below certain threshold
        if A in tankingTeams and gamesPlayed[A] >= tankingStart:
            tankA = True
        if B in tankingTeams and gamesPlayed[A] >= tankingStart:
            tankB = True
        teamRecords, gamesPlayed, teamWinLoss = simulateMatch(
            A, B, tankA, tankB,
            teamRecords, gamesPlayed, teamWinLoss
            )

    return teamRecords, gamesPlayed, teamWinLoss

def simulateTanking():
    teamTankResults = defaultdict(list) #list of length range(38) of team's record
    teamTankGamesPlayed = defaultdict(list)
    teamTankWinLoss = defaultdict(list)
    for team in WNBA_TEAMS:
        for tankStart in range(NUM_GAMES_PER_TEAM+1):
            records, played, winLoss = simulateSeason(games,[team],tankStart)
            teamTankResults[team].append(records[team])
            teamTankGamesPlayed[team].append(played[team])
            teamTankWinLoss[team].append(winLoss[team])
    return teamTankResults, teamTankGamesPlayed, teamTankWinLoss

# simulateSeason()
