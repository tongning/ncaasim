from __future__ import division
import csv
import math
import random
import sys
import itertools


class Team:
    def __init__(self, name, predictors, known_wins):
        self.name = name
        self.predictors = predictors
        self.num_round1_wins = 0
        self.num_round2_wins = 0
        self.num_round3_wins = 0
        self.num_round4_wins = 0
        self.num_round5_wins = 0
        self.num_championship_wins = 0
        self.known_wins = known_wins

    def __str__(self):
        return self.name


class Match:

    def __init__(self, team1, team2, known_winner=None):
        self.team1 = team1
        self.team2 = team2

        if known_winner is None:
            # Calculate team1's win probability
            team1_predictors = self.team1.predictors
            team2_predictors = self.team2.predictors
            predictor_differences = []
            for idx, predictor in enumerate(team1_predictors):
                predictor_differences.append(predictor - team2_predictors[idx])
            exponent = 0
            exponent += constant
            for idx in range(num_predictors):
                exponent += predictor_coefficients[idx] * predictor_differences[idx]
            odds_team1_wins = math.e ** exponent
            self.probability_team_one_wins = odds_team1_wins / (1.0 + odds_team1_wins)

            # Now pick a winner!
            rand_num = random.random()
            if rand_num <= self.probability_team_one_wins:
                self.winner = self.team1
            else:
                self.winner = self.team2
        else:
            self.winner = known_winner
            if self.winner == self.team1:
                self.probability_team_one_wins = 1
            else:
                self.probability_team_one_wins = 0

    def __str__(self):
        if not self.winner:
            self.winner = "Unknown"
        return "Match: "+self.team1.name+" vs. "+self.team2.name+"\nProbability former team wins is " + \
            str(self.probability_team_one_wins) + "\nWinner is: " + str(self.winner)+"\n"

matches = [None] * 63
predictor_coefficients = []
all_csv_rows = []
teams = []
non_playing_teams = []
with open('settings.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')

    num_runs_row = next(csv_reader)
    num_runs = int(num_runs_row[1])

    round_of_row = next(csv_reader)
    round_of = int(round_of_row[1])

    num_predictors_row = next(csv_reader)
    num_predictors = int(num_predictors_row[1])

    constant_row = next(csv_reader)
    constant = float(constant_row[1])

    for i in range(num_predictors):
        predictor_coefficient_row = next(csv_reader)
        predictor_coefficients.append(float(predictor_coefficient_row[1]))

    # Skip a heading row
    next(csv_reader)

    # Create team objects
    finished_bracket_teams = False
    while True:
        try:
            team_row = next(csv_reader)
        except StopIteration:
            break

        if team_row[0] == 'Not on bracket':
            finished_bracket_teams = True
            continue

        team_name = team_row[1]
        team_known_wins = int(team_row[2])
        team_predictor_values = []
        column_num = 3
        while team_row[column_num] != '':
            team_predictor_values.append(float(team_row[column_num]))
            column_num += 1

        new_team = Team(team_name, team_predictor_values, team_known_wins)
        if not finished_bracket_teams:
            teams.append(new_team)
        else:
            non_playing_teams.append(new_team)

    # Error check
    # Make sure "Round of" value is valid - 64, 32, 16, 8, or 2
    valid_round_ofs = [64, 32, 16, 8, 2]
    if round_of not in valid_round_ofs:
        print("Error: The ROUND OF value specified in your CSV is invalid.")
        print("Value should be 64, 32, 16, 8, or 2.")
        print("Please double-check your CSV and relaunch this program.")
        print("RUN FAILED - INPUT ERROR")
        input()
        sys.exit()

    # Error check
    # Make sure number of teams in the spreadsheet matches "Round of" value
    if len(teams) != round_of:
        print("Error: Are you sure this is a round of "+str(round_of)+"?")
        print("You've listed "+str(len(teams))+" teams in the CSV.")
        print("Please double-check your CSV and relaunch this program.")
        print("RUN FAILED - INPUT ERROR")
        input()
        sys.exit()

    for j in range(num_runs):
        # Run through first round matches, # 0-31
        team1_idx = 0
        team2_idx = 1
        match_num = 0
        while team2_idx < len(teams):
            # Does either team already have 1 or more wins so far?
            # If so, they've already won round 1 match; force winner

            if teams[team1_idx].known_wins >= 1:  # We already know team 1 won this
                matches[match_num] = Match(teams[team1_idx], teams[team2_idx], teams[team1_idx])
            elif teams[team2_idx].known_wins >= 1:  # We already know team 2 won this
                matches[match_num] = Match(teams[team1_idx], teams[team2_idx], teams[team2_idx])
            else:  # Determine winner by probability
                matches[match_num] = Match(teams[team1_idx], teams[team2_idx])

            matches[match_num].winner.num_round1_wins += 1

            team1_idx += 2
            team2_idx += 2
            match_num += 1

        # Run through second round matches, # 32-47

        for idx in range(32, 48):
            # Does either team already have 2 or more wins so far?
            # If so, they've already won round 2 match; force winner

            if matches[2*idx-64].winner.known_wins >= 2:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner, matches[2*idx-64].winner)
            elif matches[2*idx-64+1].winner.known_wins >= 2:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner, matches[2*idx-64+1].winner)
            else:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner)

            matches[idx].winner.num_round2_wins += 1

        # Run through third round matches, # 48-55
        for idx in range(48, 56):

            # Does either team already have 3 or more wins so far?
            # If so, they've already won round 3 match; force winner

            if matches[2*idx-64].winner.known_wins >= 3:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner, matches[2*idx-64].winner)
            elif matches[2*idx-64+1].winner.known_wins >= 3:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner, matches[2*idx-64+1].winner)
            else:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner)

            matches[idx].winner.num_round3_wins += 1

        # Run through fourth round matches, # 56-59
        for idx in range(56, 60):

            # Does either team already have 4 or more wins so far?
            # If so, they've already won round 4 match; force winner

            if matches[2*idx-64].winner.known_wins >= 4:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner, matches[2*idx-64].winner)
            elif matches[2*idx-64+1].winner.known_wins >= 4:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner, matches[2*idx-64+1].winner)
            else:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner)

            matches[idx].winner.num_round4_wins += 1

        # 60 and 61
        for idx in range(60, 62):

            # Does either team already have 5 or more wins so far?
            # If so, they've already won round 5 match; force winner
            if matches[2*idx-64].winner.known_wins >= 5:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner, matches[2*idx-64].winner)
            elif matches[2*idx-64+1].winner.known_wins >= 5:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner, matches[2*idx-64+1].winner)
            else:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner)

            matches[idx].winner.num_round5_wins += 1

        # Championship, # 62
        for idx in range(62, 63):
            # Does either team already have 6 or more wins so far?
            # If so, they've already won championship match; force winner
            if matches[2*idx-64].winner.known_wins >= 6:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner, matches[2*idx-64].winner)
            elif matches[2*idx-64+1].winner.known_wins >= 6:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner, matches[2*idx-64+1].winner)
            else:
                matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner)

            matches[idx].winner.num_championship_wins += 1

    with open('out.csv', "w", newline='') as out_file:
        writer = csv.writer(out_file, delimiter=',')
        for team in teams:
            writer.writerow([team, str(team.num_round1_wins/num_runs), str(team.num_round2_wins/num_runs),
                             str(team.num_round3_wins/num_runs), str(team.num_round4_wins/num_runs),
                             str(team.num_round5_wins/num_runs), str(team.num_championship_wins/num_runs)])

    # Generate all possible pairings
    # Join the non-playing teams into the teams list
    teams = teams + non_playing_teams
    combinations = itertools.combinations(teams, 2)
    all_matches = []
    for combination in combinations:
        all_matches.append(Match(combination[0], combination[1]))

    with open('all_matches.csv', "w", newline='') as out_file:
        writer = csv.writer(out_file, delimiter=',')
        writer.writerow(["First team", "Second team", "Probability First Team Wins"])
        for match in all_matches:
            writer.writerow([match.team1, match.team2, match.probability_team_one_wins])


    # Print results for each team
    for match in matches:
        print(match)
    for team in teams:
        print(team)

        print("Winning round 1:\t"+str(team.num_round1_wins/num_runs))
        print("Winning round 2:\t"+str(team.num_round2_wins/num_runs))
        print("Winning round 3:\t"+str(team.num_round3_wins/num_runs))
        print("Winning round 4:\t"+str(team.num_round4_wins/num_runs))
        print("Winning round 5:\t"+str(team.num_round5_wins/num_runs))
        print("Winning Championship:\t"+str(team.num_championship_wins/num_runs))