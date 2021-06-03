"""
This file contains the draft strategies.
"""

import numpy as np
from collections import defaultdict
from simulation import WNBA_TEAMS
from typing import List, Dict

def computeStandings(teamRecords: Dict[str, np.array]):
	"""
	Computes the standings at the end of the WNBA season.

	Returns an ordered list with all teams in WNBA_TEAMS,
		where the first team had the best record, and so on.
	"""
	# TODO: do we care about tiebreakers? 
	# Or do we just say that teams with the same record are ordered the same
	recordsOrdered = [teamRecords[team] for team in WNBA_TEAMS]

	standings = [
		team for _, team in sorted(zip(teamRecords, WNBA_TEAMS), reverse=True)
	]

	return standings

def computeWeightedStandings(teamWinLoss: Dict[str, np.array], weights: np.array):
	"""
	This function computes standings in which each win is weighted different.

	teamWinLoss is a dict from team to np.array, where each 1 is a win and each 0 is a loss

	We assume that weights is an np.array of length the number of games in the season.
	"""
	weightedRecords = [np.dot(teamWinLoss[team], weights) for team in WNBA_TEAMS]

	standings = [
		team for _, team in sorted(zip(weightedRecords, WNBA_TEAMS), reverse=True)
	]

	return standings

def generateTeamPreferences(nPlayers: int, noise: int = 1) -> Dict[str, List[int]]:
	"""
	Generate the preferences of each team across players.

	Team i has utility |j + Uniform[0, noise]| for player j.
	"""
	preferences = defaultdict(list)
	playerList = list(range(nPlayers))

	for team in WNBA_TEAMS:
		utilities = [
			j + np.random.uniform(low=0, high=noise) for j in range(nPlayers)
		]
		preferences[team] = [
			player for _, player in sorted(zip(utilities, playerList))
		]

	return preferences

def runClassicDraft(standings: List[str], nPlayers: int = 30, noise: int = 1):
	"""
	Classic "backwards" draft in reverse order of the standings.

	Returns a dict from team to the rank of the player they got (according to their preferences).
	"""

	# initialize the variables we will use
	draftOrder = standings[::-1]
	draftResults = defaultdict(int) # team -> rank of player drafted
	teamPreferences = generateTeamPreferences(nPlayers, noise)
	teamPreferencesCopy = {team: prefs[::] for team, prefs in teamPreferences.items()}

	for team in draftOrder:
		offer = teamPreferences[team][0]
		
		draftResults[team] = teamPreferencesCopy[team].index(offer) + 1

		# remove that player from all other team preferences
		[teamPreferences[team].remove(offer) for team in WNBA_TEAMS]

	return draftResults

def runBucketedDraft(
	nOffers: int,
	standings: List[str],
	teamRecords: Dict[str, np.array],
	nPlayers: int = 30,
	noise: int = 1
	):
	"""
	Run the bucketed draft system.

	Returns a dict from team to the rank of the player they got (according to their preferences).

	At each step,
	- The worse |nOffers| teams that haven't found their pick for that round make offers to their top prospects
	- Each player that has an offer permanently accepts one
	"""
	draftResults = defaultdict(int) # team -> rank of player drafted
	teamPreferences = generateTeamPreferences(nPlayers, noise)
	teamPreferencesCopy = {team: prefs[::] for team, prefs in teamPreferences.items()}

	while len(standings) > 0:
		worstTeams = standings[-nOffers:]
		offers = {
			team: teamPreferences[team][0] for team in worstTeams
		}
		# get offers for all players
		playerOptions = defaultdict(list)
		for team, player in offers.items():
			playerOptions[player].append(team)

		# each player accepts their best offer
		for player, options in playerOptions.items():
			# each team has probability of getting picked proportinal to their #wins.
			teamWeights = np.array([teamRecords[team] + .1 for team in options])
			teamWeights = teamWeights / np.sum(teamWeights)
			
			chosenTeam = options[np.random.choice(len(teamWeights), p=teamWeights)]

			draftResults[chosenTeam] = teamPreferencesCopy[chosenTeam].index(player) + 1
			standings.remove(chosenTeam)
			
			# remove that player from all other team preferences
			[teamPreferences[team].remove(player) for team in WNBA_TEAMS]

	return draftResults




