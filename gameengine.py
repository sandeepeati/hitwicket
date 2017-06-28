
import random
import time
from team import teams
from innings import innings
import os

rows, columns = os.popen('stty size', 'r').read().split()
columns = int(columns)

class gameplay:
    def __init__(self):
        self.team1_name = input('\nEnter your team1 name: \n')
        self.team2_name = input('Enter your team2 name: \n')
        self.order = [None, None]
        self.inning1_stats = None
        self.inning2_stats = None

    def preplay(self):
        self.team1, self.team2 = teams().generate_team()

        def toss():
            team1_toss = input('Choose Heads(h) or Tails(t): ').lower()
            toss_result = str(random.choice('ht'))

            if team1_toss == toss_result and team1_toss in 'ht':
                self.order = [self.team1_name, self.team2_name]
            elif team1_toss != toss_result and team1_toss in 'ht':
                self.order = [self.team2_name, self.team1_name]
            else:
                return toss()

            team1_toss = 'Heads' if team1_toss == 'h' else 'Tails'
            toss_result = 'Heads' if toss_result == 'h' else 'Tails'
            print('-'*int(columns))
            print('\n',  self.team2[0][0] + ' spins the coin and ' + self.team1[0][0] + ' calls ' + team1_toss + '. ' + toss_result + ' it is.', '\n')
            print('\n', self.order[0] + ' win and decide to bat first')
            print('-'*int(columns))

        toss()



    def play(self):

        bat = self.team1 if self.order[0] == self.team1_name else self.team2
        bowl = self.team1 if self.order[1] == self.team1_name else self.team2

        self.first_innings, self.inning1_stats = innings(self.order[0] , bat, bowl, 1)
        print('\n\n','End of First Innings...')
        print('Second Innings will begin in a minute...','\n\n')
        time.sleep(30)
        self.second_innings, self.inning2_stats = innings(self.order[1], bowl, bat, 2, int(self.first_innings[0]))

    def postplay(self):
        inning1_bat = self.inning1_stats[0]
        inning1_bowl = self.inning1_stats[1]
        inning1_bat_top3 = sorted(inning1_bat, key= lambda x: x[1])[::-1]
        inning1_bowl_top3 = sorted(inning1_bowl, key= lambda x: x[3])[::-1]

        inning2_bat = self.inning2_stats[0]
        inning2_bowl = self.inning2_stats[1]
        inning2_bat_top3 = sorted(inning2_bat, key= lambda x: x[1])[::-1]
        inning2_bowl_top3 = sorted(inning2_bowl, key= lambda x: x[3])[::-1]

        print('\n\n')
        print('-'*columns)
        print(self.order[0].ljust(columns-25), str(self.first_innings[2]) + ' OVERS','  ', self.first_innings[0], '-', self.first_innings[1])
        print('-'*columns)
        print('\n')
        print(str(inning1_bat_top3[0][0]).ljust(20),'  ', str(inning1_bat_top3[0][1]).ljust(5), '(',str(inning1_bat_top3[0][2]).ljust(3),')', '\t\t', str(inning1_bowl_top3[0][0]).ljust(20), '  ',str(inning1_bowl_top3[0][2]).ljust(5),'-',str(inning1_bowl_top3[0][3]).ljust(2))
        print('\n')
        print(str(inning1_bat_top3[1][0]).ljust(20),'  ', str(inning1_bat_top3[1][1]).ljust(5), '(',str(inning1_bat_top3[1][2]).ljust(3),')', '\t\t', str(inning1_bowl_top3[1][0]).ljust(20), '  ',str(inning1_bowl_top3[1][2]).ljust(5),'-',str(inning1_bowl_top3[1][3]).ljust(2))
        print('\n')
        print(str(inning1_bat_top3[2][0]).ljust(20),'  ', str(inning1_bat_top3[2][1]).ljust(5), '(',str(inning1_bat_top3[2][2]).ljust(3),')')
        print('-'*columns)
        print('\n')

        print('-'*columns)
        print(self.order[1].ljust(columns-25), str(self.second_innings[2]) + ' OVERS','  ', self.second_innings[0], '-', self.second_innings[1])
        print('-'*columns)
        print('\n')
        print(str(inning2_bat_top3[0][0]).ljust(20),'  ', str(inning2_bat_top3[0][1]).ljust(5), '(',str(inning2_bat_top3[0][2]).ljust(3),')', '\t\t', str(inning2_bowl_top3[0][0]).ljust(20), '  ',str(inning2_bowl_top3[0][2]).ljust(5),'-',str(inning2_bowl_top3[0][3]).ljust(2))
        print('\n')
        print(str(inning2_bat_top3[1][0]).ljust(20),'  ', str(inning2_bat_top3[1][1]).ljust(5), '(',str(inning2_bat_top3[1][2]).ljust(3),')', '\t\t', str(inning2_bowl_top3[1][0]).ljust(20), '  ',str(inning2_bowl_top3[1][2]).ljust(5),'-',str(inning2_bowl_top3[1][3]).ljust(2))
        print('\n')
        print(str(inning2_bat_top3[2][0]).ljust(20),'  ', str(inning2_bat_top3[2][1]).ljust(5), '(',str(inning2_bat_top3[2][2]).ljust(3),')')
        print('-'*columns)
        if self.first_innings[0] > self.second_innings[0]:
            m = self.order[0] + ' wins by ' + str(self.first_innings[0] - self.second_innings[0]) + ' runs.'
        elif self.first_innings[0] < self.second_innings[0]:
            m = self.order[1] + ' wins by ' + str(10 - self.second_innings[1]) + ' wickets.'
        else:
            m = 'Match draw.'
        print(m.center(columns))
        print('-'*columns)
        print('\n')



match = gameplay()
match.preplay()
match.play()
match.postplay()

