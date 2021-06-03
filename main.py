"""
This file contains the main code to run our draft simulautions
"""

import numpy as np
from collections import defaultdict
from typing import List, Dict
import itertools as it
from tqdm import tqdm

from simulation import (
	WNBA_TEAMS, simulateSeason, createGames
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
	B = 100

	# vanilla draft
	positionVSPreference = {team: [] for team in WNBA_TEAMS for i in range(39)}

	for tankingTeam in WNBA_TEAMS:
		for tankingStart in range(0, 38 + 1):
			for _ in range(B):
				teamRecords, gamesPlayed, teamWinLoss = simulateSeason([tankingTeam], tankingStart)

				standings = computeStandings(teamRecords)

				draftResults = runClassicDraft(standings, noise=5)

				# compiling results: keep track standings vs draft pick
				for team in standings:
					positionVSPreference[tankingTeam].append(draftResults[tankingTeam])

	print({team: np.mean(pos) for team, pos in positionVSPreference.items()})

	return

	# bucketed draft
	positionVSPreference = {team: [] for team in WNBA_TEAMS}
	
	for _ in range(B):
		teamRecords, gamesPlayed, teamWinLoss = simulateSeason()

		standings = computeStandings(teamRecords)

		draftResults = runBucketedDraft(4, standings[::], teamRecords, noise=5)

		# compiling results: keep track standings vs draft pick
		for team in standings:
			positionVSPreference[team].append(draftResults[team])

	print({team: np.mean(pos) for team, pos in positionVSPreference.items()})

full_simulation_no_tanking()