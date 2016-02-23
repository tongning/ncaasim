from __future__ import division
import csv
import math
import random

class Team:
    def __init__(self, name, predictors):
        self.name = name
        self.predictors = predictors
        self.num_round1_wins = 0
        self.num_round2_wins = 0
        self.num_round3_wins = 0
        self.num_round4_wins = 0
        self.num_round5_wins = 0
        self.num_championship_wins = 0

    def __str__(self):
        return self.name


class Match:

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
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
        #print(str(self))


    def __str__(self):
        if not self.winner:
            self.winner = "Unknown"
        return "Match: "+self.team1.name+" vs. "+self.team2.name+"\nProbability former team wins is "+\
                str(self.probability_team_one_wins)+"\nWinner is: "+str(self.winner)+"\n"


num_runs = 1

matches = [None] * 63
predictor_coefficients = []
all_csv_rows = []
teams = []
with open('settings.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')

    first_row = next(csv_reader)
    num_predictors = int(first_row[1])
    second_row = next(csv_reader)
    constant = float(second_row[1])
    for i in range(num_predictors):
        predictor_coefficient_row = next(csv_reader)
        predictor_coefficients.append(float(predictor_coefficient_row[1]))

    # Skip a heading row
    next(csv_reader)

    # Create team objects

    while True:
        try:
            team_row = next(csv_reader)
        except StopIteration:
            break

        team_name = team_row[1]
        team_predictor_values = []
        column_num = 2
        while team_row[column_num] != '':
            team_predictor_values.append(float(team_row[column_num]))
            column_num += 1

        new_team = Team(team_name, team_predictor_values)
        teams.append(new_team)

    for j in range(num_runs):
        # Run through first round matches, # 0-31
        team1_idx = 0
        team2_idx = 1
        match_num = 0
        while team2_idx < len(teams):
            matches[match_num] = Match(teams[team1_idx], teams[team2_idx])
            matches[match_num].winner.num_round1_wins += 1
            #print(matches[match_num])
            team1_idx += 2
            team2_idx += 2
            match_num += 1

        # Run through second round matches, # 32-47
        for idx in range(32, 48):
            matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner)
            matches[idx].winner.num_round2_wins += 1
            #print(matches[idx])


        # Run through third round matches, # 48-55
        for idx in range(48, 56):
            matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner)
            matches[idx].winner.num_round3_wins += 1
            #print(matches[idx])

        # Run through fourth round matches, # 56-59
        for idx in range(56, 60):
            matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner)
            matches[idx].winner.num_round4_wins += 1
            #print(matches[idx])

        # 60 and 61
        for idx in range(60, 62):
            matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner)
            matches[idx].winner.num_round5_wins +=1
            #print(matches[idx])

        # Championship, # 62
        for idx in range(62, 63):
            matches[idx] = Match(matches[2*idx-64].winner, matches[2*idx-64+1].winner)
            matches[idx].winner.num_championship_wins += 1
            #print(matches[idx])

    with open('out.csv', "w", newline='') as out_file:
        writer = csv.writer(out_file, delimiter=',')
        for team in teams:
            writer.writerow([team, str(team.num_round1_wins/num_runs),str(team.num_round2_wins/num_runs),str(team.num_round3_wins/num_runs),str(team.num_round4_wins/num_runs),str(team.num_round5_wins/num_runs),str(team.num_championship_wins/num_runs)])
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

    #for match in matches:
    #    print(match)




























