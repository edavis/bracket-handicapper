#!/usr/bin/env python3

# some concepts borrowed from https://github.com/stahl085/bracketology

import csv
import random
from operator import itemgetter
from collections import (
    defaultdict, Counter
)

random.seed(2020-21)

# 3/18 -> R68 finished
# 3/19 -> D1 R64 finished
# 3/20 -> D2 R64 finished
# 3/21 -> D1 R32 finished
# 3/22 -> D2 R32 finished

# 3/27 -> D1 S16 finished
# 3/28 -> D2 S16 finished
# 3/29 -> D1 E8 finished
# 3/30 -> D2 E8 finished

def info(s=''):
    if DEBUG: print(s)

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
        self.winner = None # make deterministic
        self.points_lookup = {
            2: 1,
            3: 2,
            4: 4,
            5: 8,
            6: 16,
            7: 32,
        }

    def Points(self):
        return self.points_lookup[self.round_number]

    def Winner(self):
        if self.winner is not None:
            return self.winner

        rnd = 'rd%d_win' % self.round_number
        top_win = float(self.top_team.stats[rnd])
        bot_win = float(self.bottom_team.stats[rnd])

        top_rtg = float(self.top_team.stats['team_rating'])
        bot_rtg = float(self.bottom_team.stats['team_rating'])

        if top_win == 0.0:
            info(f'{self.top_team} lost in round {self.round_number}, making {self.bottom_team} the winner')
            self.winner = self.bottom_team
            return self.bottom_team
        elif bot_win == 0.0:
            info(f'{self.bottom_team} lost in round {self.round_number}, making {self.top_team} the winner')
            self.winner = self.top_team
            return self.top_team
        else:
            # Refs <https://fivethirtyeight.com/features/how-our-march-madness-predictions-work-2/>
            d = -(top_rtg - bot_rtg)
            d = d * 30.464 / 400.0
            p = 1.0 / (1.0 + 10**d)
            r = random.random()
            choice = self.top_team if r < p else self.bottom_team
            info(f'Giving {self.top_team} a {p} chance of beating {self.bottom_team}. With a roll of {r}, picking {choice}.')
            self.winner = choice
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
        round1_str = 'Round of 64: ' + ', '.join([str(game) for game in self.Round1])
        round2_str = '\nRound of 32: ' + ', '.join([str(game) for game in self.Round2])
        round3_str = '\nSweet 16: ' + ', '.join([str(game) for game in self.Round3])
        round4_str = '\nElite 8: ' + ', '.join([str(game) for game in self.Round4])
        winner_str = '\nFinal 4: ' + str(self.Winner)
        return f'{round1_str}{round2_str}{round3_str}{round4_str}{winner_str}'

class FinalFour():
    def __init__(self, west, east, south, midwest):
        # the winners out of each region
        self.west = west
        self.east = east
        self.south = south
        self.midwest = midwest

    def Simulate(self):
        self.Game16 = Game(self.west, self.east, 6)
        self.Game17 = Game(self.south, self.midwest, 6)
        self.Round5 = [
            self.Game16, self.Game17
        ]

        self.Game18 = Game(self.Game16.Winner(), self.Game17.Winner(), 7)
        self.Round6 = [
            self.Game18
        ]

        self.Winner = self.Game18.Winner()

    def __repr__(self):
        round1_str = 'Final Four: ' + ', '.join([str(game) for game in self.Round5])
        round2_str = '\nChampionship: ' + ', '.join([str(game) for game in self.Round6])
        winner_str = '\nChampion: ' + str(self.Winner)
        return f'{round1_str}{round2_str}{winner_str}'

def run_simulation(teams):
    regions = {}
    for region_name in teams.keys():
        assert len(teams[region_name]) == 16, 'invalid number of teams in region'
        region_teams = [team for seed, team in sorted(teams[region_name].items())]
        info(f'{region_name} Region\n' + '-' * 50)
        regions[region_name] = Region(region_name, region_teams)
        regions[region_name].Simulate()
        info(regions[region_name])
        info()

    info('Final Four\n' + '-' * 50)
    ff = FinalFour(
        regions['West'].Winner,
        regions['East'].Winner,
        regions['South'].Winner,
        regions['Midwest'].Winner,
    )
    ff.Simulate()
    info(ff)
    info()

    # ---------------------------------------------------------------------------

    reader = csv.DictReader(open('brackets.csv'))

    # Add a bit of jitter between [0, 1) to break ties
    points = defaultdict(random.random)

    for row in reader:
        region_name = row.pop('Region')
        region = ff if region_name in ['Final Four', 'Champion'] else regions[region_name]

        game_label = row.pop('Game')
        game = getattr(region, game_label)

        for player in row.keys():
            game_points = int(row[player] == game.winner.name) * game.Points()
            info(f"[{region_name} {game_label}] {player}'s Pick: {row[player]}, Outcome: {game.winner}, Points: {game_points}")
            points[player] += game_points

    info(f'Simulation Finished = {points}')
    return points

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-n', '--iterations', default=10_000, type=int)
    parser.add_argument('latest')
    args = parser.parse_args()

    DEBUG = args.debug
    LATEST_RESULTS = args.latest
    iterations = args.iterations
    finishes = {}

    # Make sure everybody is displayed
    reader = csv.DictReader(open('brackets.csv'))
    row = next(reader)
    row.pop('Region')
    row.pop('Game')
    finishes.update({player: Counter() for player in row.keys()})

    # ---------------------------------------------------------------------------
    # Downloaded from <https://projects.fivethirtyeight.com/march-madness-api/2021/fivethirtyeight_ncaa_forecasts.csv>
    reader = csv.DictReader(open('fivethirtyeight_ncaa_forecasts.csv'))
    teams = {
        'West': {},
        'East': {},
        'South': {},
        'Midwest': {},
    }

    for row in reader:
        if row['gender'] != 'mens' or row['forecast_date'] != LATEST_RESULTS: continue # only use the latest mens
        if row['playin_flag'] == '1' and row['rd1_win'] == '0.0': continue # team out before Friday

        region = row['team_region']
        seed = int(row['team_seed'].rstrip('ab'))
        team = row['team_name']
        teams[region][seed] = Team(team, seed, row)
    # ---------------------------------------------------------------------------

    for iteration in range(iterations):
        simulation = run_simulation(teams)
        rank = [player for player, score in sorted(simulation.items(), key=itemgetter(1), reverse=True)]

        for player, score in simulation.items():
            ordinal = rank.index(player) + 1
            finishes[player].update([ordinal])

        if (iteration + 1) % 500 == 0: print('.', end='', flush=True)

    print()

    fieldnames = ['Player']
    fieldnames += list(range(1, 17))
    writer = csv.DictWriter(open('finishes.csv', 'w'), fieldnames=fieldnames)
    writer.writeheader()
    for player, counts in finishes.items():
        fields = {k: v / iterations for k, v in dict(counts).items()}
        obj = {'Player': player}
        obj.update(fields)
        writer.writerow(obj)
