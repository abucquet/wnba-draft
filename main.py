"""
This file contains the main code to run our draft simulautions
"""

import numpy as np
from collections import defaultdict
from typing import List, Dict
import itertools as it
from tqdm import tqdm
import matplotlib.pyplot as plt

from simulation import (
	WNBA_TEAMS, NUM_GAMES_PER_TEAM, simulateSeason, createGames, elo
	)
from drafts import (
	computeStandings, computeWeightedStandings, runClassicDraft, runBucketedDraft
	)

def full_simulation_no_tanking():
	B = 100

	# vanilla draft
	positionVSPreference = [[] for team in WNBA_TEAMS]

	for _ in range(B):
		teamRecords, gamesPlayed, teamWinLoss = simulateSeason()

		standings = computeStandings(teamRecords)

		draftResults = runClassicDraft(standings, noise=5)

		# compiling results: keep track standings vs draft pick
		for i, team in enumerate(standings):
			positionVSPreference[team].append(draftResults[team])

	print([np.mean(pos) for pos in positionVSPreference])

	# bucketed draft
	positionVSPreference = [[] for team in WNBA_TEAMS]
	
	for _ in range(B):
		teamRecords, gamesPlayed, teamWinLoss = simulateSeason()

		standings = computeStandings(teamRecords)

		draftResults = runBucketedDraft(4, standings[::], teamRecords, noise=5)

		# compiling results: keep track standings vs draft pick
		for i, team in enumerate(standings):
			positionVSPreference[i].append(draftResults[team])

	print([np.mean(pos) for pos in positionVSPreference])

def full_simulation_with_tanking():
	B = 1000

	# vanilla draft
	draftPreference = {team: [] for team in WNBA_TEAMS for i in range(1, NUM_GAMES_PER_TEAM + 2)}
	standingResults = {team: [] for team in WNBA_TEAMS for i in range(1, NUM_GAMES_PER_TEAM + 2)}

	for tankingTeam in tqdm(WNBA_TEAMS):
		for tankingStart in range(1, NUM_GAMES_PER_TEAM + 2):
			average_choice = 0
			average_standing = 0
			for _ in range(B):
				teamRecords, gamesPlayed, teamWinLoss = simulateSeason([tankingTeam], tankingStart)

				standings = computeStandings(teamRecords)
				average_standing += standings.index(tankingTeam)

				draftResults = runClassicDraft(standings, noise=5)
				average_choice += draftResults[tankingTeam]

			# compiling results: keep track standings vs draft pick
			draftPreference[tankingTeam].append(average_choice/B)
			standingResults[tankingTeam].append(average_standing/B)

	for team in WNBA_TEAMS:
		plt.figure()
		plt.plot(
			list(range(1, NUM_GAMES_PER_TEAM + 2)), standingResults[team],
			color="red",
			label="Average Standing"
			)
		plt.plot(
			list(range(1, NUM_GAMES_PER_TEAM + 2)), draftPreference[team],
			color="blue",
			label="Average Player Choice"
			)
		plt.ylabel("Average Position")
		plt.xlabel("Tanking Starting at Game")
		plt.title(f"Tanking Strategy for {team} (elo={elo[team]})")
		plt.legend()
		plt.savefig("plots/" + team + "_regular" + ".png")
		plt.close()


	# bucketed draft
	draftPreference = {team: [] for team in WNBA_TEAMS for i in range(1, NUM_GAMES_PER_TEAM + 2)}
	standingResults = {team: [] for team in WNBA_TEAMS for i in range(1, NUM_GAMES_PER_TEAM + 2)}

	for tankingTeam in tqdm(WNBA_TEAMS):
		for tankingStart in range(0, NUM_GAMES_PER_TEAM + 1):
			average_choice = 0
			average_standing = 0
			for _ in range(B):
				teamRecords, gamesPlayed, teamWinLoss = simulateSeason([tankingTeam], tankingStart)

				standings = computeStandings(teamRecords)
				average_standing += standings.index(tankingTeam)

				draftResults = runBucketedDraft(4, standings[::], teamRecords, noise=5)
				average_choice += draftResults[tankingTeam]

			# compiling results: keep track standings vs draft pick
			draftPreference[tankingTeam].append(average_choice/B)
			standingResults[tankingTeam].append(average_standing/B)

	for team in WNBA_TEAMS:
		plt.figure()
		plt.plot(
			list(range(1, NUM_GAMES_PER_TEAM + 2)), standingResults[team],
			color="red",
			label="Average Standing"
			)
		plt.plot(
			list(range(1, NUM_GAMES_PER_TEAM + 2)), draftPreference[team],
			color="blue",
			label="Average Player Choice"
			)
		plt.ylabel("Average Position")
		plt.xlabel("Tanking Starting at Game")
		plt.title(f"Tanking Strategy for {team} (elo={elo[team]})")
		plt.legend()
		plt.savefig("plots/" + team + "_bucketed" + ".png")
		plt.close()

full_simulation_with_tanking()