#!/usr/bin/env python3

# some concepts borrowed from https://github.com/stahl085/bracketology

import csv
import random

class Team():
    def __init__(self, name, seed, stats):
        self.name = name
        self.seed = seed
        self.stats = stats

    def __repr__(self):
        return f"#{self.seed} {self.name}"

class Game():
    def __init__(self, top_team, bottom_team, round_number):
        self.top_team = top_team
        self.bottom_team = bottom_team
        self.round_number = round_number

    def Winner(self):
        rnd = 'rd%d_win' % self.round_number
        top_win = float(self.top_team.stats[rnd])
        bot_win = float(self.bottom_team.stats[rnd])

        top_rtg = float(self.top_team.stats['team_rating'])
        bot_rtg = float(self.bottom_team.stats['team_rating'])

        #print(f'{self.top_team} = {top_win}, {self.bottom_team} = {bot_win} (round = {self.round_number})')

        if top_win == 0.0:
            print(f'{self.top_team} lost in round {self.round_number}, making {self.bottom_team} the winner')
            return self.bottom_team
        elif bot_win == 0.0:
            print(f'{self.bottom_team} lost in round {self.round_number}, making {self.top_team} the winner')
            return self.top_team
        else:
            # Refs <https://fivethirtyeight.com/features/how-our-march-madness-predictions-work-2/>
            d = -(top_rtg - bot_rtg)
            d = d * 30.464 / 400.0
            p = 1.0 / (1.0 + 10**d)
            r = random.random()
            choice = self.top_team if r < p else self.bottom_team
            print(f'Giving {self.top_team} a {p} chance of beating {self.bottom_team}. With a roll of {r}, picking {choice}.')
            return choice

    def __repr__(self):
        return f"<Round {self.round_number}: {self.top_team} vs {self.bottom_team}>"

class Region():
    def __init__(self, name, teams):
        assert len(teams) == 16, 'wrong number of teams'
        self.Name = name
        self.Teams = teams

        self.Game1 = Game(teams[1-1], teams[16-1], 2)
        self.Game2 = Game(teams[8-1], teams[9-1], 2)
        self.Game3 = Game(teams[5-1], teams[12-1], 2)
        self.Game4 = Game(teams[4-1], teams[13-1], 2)
        self.Game5 = Game(teams[6-1], teams[11-1], 2)
        self.Game6 = Game(teams[3-1], teams[14-1], 2)
        self.Game7 = Game(teams[7-1], teams[10-1], 2)
        self.Game8 = Game(teams[2-1], teams[15-1], 2)
        self.Round1 = [
            self.Game1, self.Game2, self.Game3, self.Game4,
            self.Game5, self.Game6, self.Game7, self.Game8,
        ]
        self.Round2 = []
        self.Round3 = []
        self.Round4 = []

    def Simulate(self):
        # R2
        self.Game9 = Game(self.Game1.Winner(), self.Game2.Winner(), 3)
        self.Game10 = Game(self.Game3.Winner(), self.Game4.Winner(), 3)
        self.Game11 = Game(self.Game5.Winner(), self.Game6.Winner(), 3)
        self.Game12 = Game(self.Game7.Winner(), self.Game8.Winner(), 3)
        self.Round2 = [
            self.Game9, self.Game10, self.Game11, self.Game12
        ]

        # S16
        self.Game13 = Game(self.Game9.Winner(), self.Game10.Winner(), 4)
        self.Game14 = Game(self.Game11.Winner(), self.Game12.Winner(), 4)
        self.Round3 = [
            self.Game13, self.Game14
        ]

        # E8
        self.Game15 = Game(self.Game13.Winner(), self.Game14.Winner(), 5)
        self.Round4 = [
            self.Game15
        ]
        self.Winner = self.Game15.Winner()

    def __repr__(self):
        region_header = f'{self.Name} Region\n--------------------\n'
        round1_str = 'Round 1: ' + ', '.join([str(game) for game in self.Round1])
        round2_str = '\nRound 2: ' + ', '.join([str(game) for game in self.Round2])
        round3_str = '\nSweet 16: ' + ', '.join([str(game) for game in self.Round3])
        round4_str = '\nElite 8: ' + ', '.join([str(game) for game in self.Round4])
        winner_str = '\nFinal 4: ' + str(self.Winner)
        return f'{region_header}{round1_str}{round2_str}{round3_str}{round4_str}{winner_str}'

def main():
    # Downloaded from <https://projects.fivethirtyeight.com/march-madness-api/2021/fivethirtyeight_ncaa_forecasts.csv>
    reader = csv.DictReader(open('fivethirtyeight_ncaa_forecasts.csv'))
    teams = {
        'West': {},
        'East': {},
        'South': {},
        'Midwest': {},
    }
    regions = {}

    for row in reader:
        if row['gender'] != 'mens' or row['forecast_date'] != '2021-03-19': continue # only use the latest mens
        if row['playin_flag'] == '1' and row['rd1_win'] == '0.0': continue # team out before Friday

        region = row['team_region']
        seed = int(row['team_seed'].rstrip('ab'))
        team = row['team_name']
        teams[region][seed] = Team(team, seed, row)

    for region_name in teams.keys():
        region_teams = sorted(teams[region_name].items())
        region_teams = [team for seed, team in sorted(teams[region_name].items())]
        regions[region_name] = Region(region_name, region_teams)
        regions[region_name].Simulate()
        print(regions[region_name])

if __name__ == '__main__':
    main()
