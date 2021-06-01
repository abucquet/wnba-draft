"""
This file contains the main code to run our draft simulautions
"""

import numpy as np
from collections import defaultdict
from typing import List, Dict

from simulation import (
	WNBA_TEAMS, simulateSeason
	)
from drafts import (
	computeStandings, computeWeightedStandings, runClassicDraft, runBucketedDraft
	)

def main():
	B = 1000

	# vanilla draft
	positionVSPreference = [[] for _ in range(len(WNBA_TEAMS))]

	for _ in range(B):
		teamRecords, gamesPlayed, teamWinLoss = simulateSeason()

		standings = computeStandings(teamRecords)

		draftResults = runClassicDraft(standings, noise=5)

		# compiling results: keep track standings vs draft pick
		for i, team in enumerate(standings):
			positionVSPreference[i].append(draftResults[team])

	print([np.mean(pos) for pos in positionVSPreference])

	# bucketed draft
	positionVSPreference = [[] for _ in range(len(WNBA_TEAMS))]

	for _ in range(B):
		teamRecords, gamesPlayed, teamWinLoss = simulateSeason()

		standings = computeStandings(teamRecords)

		draftResults = runBucketedDraft(4, standings[::], teamRecords, noise=5)

		# compiling results: keep track standings vs draft pick
		for i, team in enumerate(standings):
			positionVSPreference[i].append(draftResults[team])

	print([np.mean(pos) for pos in positionVSPreference])

main()