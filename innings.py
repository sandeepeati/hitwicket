
import os
import random
import time
import math
import numpy
from collections import OrderedDict as od

rows, columns = os.popen('stty size', 'r').read().split()

columns = int(columns)

def innings(team_name, batting, bowling, inning, target=120*6):

    print('\n')
    print('-'*columns)
    print(team_name.upper() + ' INNINGS')
    print('-'*columns)
    print('\n')

    ##########################################################################################
    ##########################################################################################
    ##                  variables needed for the holding the state                          ##
    ##########################################################################################
    ##########################################################################################

    batting_order = sorted(batting, key= lambda x: x[1])[::-1]
    bowling_order = sorted(bowling, key= lambda x: x[2])[::-1]
    fielders = sorted(bowling, key= lambda x: x[4])[::-1]


    # dictionary to hold batsmen statistics in an given innings
    batting_statistics = od()

    # dictionary to hold bowler statistics in an given innings
    bowling_statistics = od()

    # statistics holding template creation
    for i in batting_order:
        batting_statistics[i[0]] = [i[0], 0, 0, 0, 0, 'dnb', batting.index(i)]

    inning_bat = []

    for j in bowling_order:
        bowling_statistics[j[0]] = [j[0], 0.0, 0, 0, bowling.index(j)]

    inning_bowl = []

    # last_bowler, to keep a tab
    last_bowler = None

    ############################################################################################

    ############################################################################################
    ############################################################################################
    ##         runs updating function for on-strike batsman on the end of every ball          ##
    ############################################################################################
    ############################################################################################

    def run_updation(onstrike, run):

        # not-out case
        if run != 5:
            # updating runs
            batting_statistics[onstrike][1] += run
            # updating balls
            batting_statistics[onstrike][2] += 1
            batting_statistics[on_strike][5] = 'Not Out'
            if run == 4:
                # updating 4 count
                batting_statistics[onstrike][3] += 1
            if run == 6:
                # updating 6 count
                batting_statistics[onstrike][4] += 1
        else:
            # updating balls in out case
            batting_statistics[onstrike][2] += 1
            batting_statistics[on_strike][5] = 'Out'


    ############################################################################################

    ############################################################################################
    ############################################################################################
    ## bowler selection with constraints applied(no continuous overs and no more than 4 overs)##
    ############################################################################################
    ############################################################################################

    def bowler_selection():
        print('Index'.ljust(25), 'Name'.ljust(25), 'Skill Level'.ljust(25), 'Overs'.ljust(25), '\n', sep='\t')
        # change the number to 11 for all players to be shown.
        for k in range(6):
            print(str(k).ljust(25), bowling_order[k][0].ljust(25), str(bowling_order[k][2]).ljust(25), str(bowling_statistics[bowling_order[k
            ][0]][1]).ljust(25), '\n', sep='\t')

        # to hold the bowler index that the player choose
        bowler_index = int(input('Choose the bowler: '))
        print('\n')

        choices = [_ for _ in range(11)]
        # checking that a bowler doesn't bowl more than 4 overs
        if bowler_index not in choices:
            print('-'*int(columns))
            print('That poor guy wasn\'t even listed in the squad.')
            print('-'*int(columns), '\n')
            return bowler_selection()
        elif bowling_statistics[bowling_order[bowler_index][0]][1] == 4:
            print('-'*int(columns))
            print('Maximum overs that can be bowled by a bowler is 4.')
            print('-'*int(columns), '\n')
            return bowler_selection()
        # checking that a bowler doesn't bowl continuous overs
        elif bowling_order[bowler_index][0] != last_bowler:
            return bowling_order[bowler_index][0]
        else:
            print('-'*int(columns))
            print('No bowler is allowed to bowl continuous overs.')
            print('-'*int(columns), '\n')
            return bowler_selection()

    #############################################################################################

    #############################################################################################
    #############################################################################################
    ##                       probabilistic randomness for runs                                 ##
    #############################################################################################
    #############################################################################################

    def prob_run(onstrike, bowler):
        batsman_index = batting_statistics[on_strike][6]
        bowler_index = bowling_statistics[bowler][4]

        # probabilities calculation
        bs = (batting[batsman_index][1] - 10) / 100 # batsman skill boost
        Bs = (bowling[bowler_index][2] - 10)/ 100 # bowler skill boost
        bf = (batting[batsman_index][5] - 10) / 100 # batsman form boost
        bfi = (batting[batsman_index][6] - 10) / 100 # batsman fitness boost
        Bf = (bowling[bowler_index][5] - 10) / 100 # bowler form boost
        Bfi = (bowling[bowler_index][6] - 10) / 100 # bowler fitness boost
        Ov = abs(10 - int(overs)) / 100 # overs boost
        wi = (5 - wickets) / 100 # wickets boost

        # assinging run probabilities to variables

        dot = 0.15 - ((bs + bf + bfi + Ov + wi) / 20)  + ((Bs + Bf + Bfi) / 12)
        run = 0.25 - ((bs + bf + bfi + Ov + wi) / 20)  + ((Bs + Bf + Bfi) / 12)
        three = 0.05 - ((bs + bf + bfi + Ov + wi) / 20)  + ((Bs + Bf + Bfi) / 12)
        four = 0.10 + ((bs + bf + bfi + Ov + wi) / 5) - ((Bs + Bf + Bfi) / 3)
        out = 0.10 - ((bs + bf + bfi + Ov + wi) / 5) + ((Bs + Bf + Bfi) / 3)
        six = 0.10 + ((bs + bf + bfi + Ov + wi) / 5) - ((Bs + Bf + Bfi) / 3)

        s = sum([dot, run, run,three, four, out, six])
        if s < 1:
            run += ((1 - s) / 2)
        else:
            six -= ((s - 1) / 3)
            out -= ((s - 1) / 3)
            four -= ((s - 1) / 3)
        # possible outcomes
        r = [0,1,2,3,4,5,6]
        # print(s, [dot, run, run, three, four, out, six])
        return numpy.random.choice(r, p = [dot, run, run, three, four, out, six])

    #############################################################################################

    #############################################################################################
    #############################################################################################
    ##                                   Over simulation                                       ##
    #############################################################################################
    #############################################################################################

    overs = 0.0
    total = 0
    wickets = 0

    on_strike = batting_order[0][0]
    non_strike = batting_order[1][0]

    while overs < 20.0 and wickets < 10 and total <= target:
        bowler = bowler_selection()
        print('\n')
        print('-'*columns)
        print('over ' + str(overs + 1.0) + ' to be bowled by ' + bowler)
        print('-'*columns)
        print('\n')

        for balls in range(1,7):
            run = int(prob_run(on_strike, bowler))

            # fielder selection
            fielder = fielders[random.randint(0,2)][0]

            # comments holding dict(taken from hitwicket.com)
            comments = {0: ' no run, good short ball and '+on_strike+' has to go on his toes to defend.', 1: '1 run, short of a length ball, straight, tucked away towards backward square leg for a single.' +fielder+' does well to come around fast.', 2: '2 runs, holds back the length, '+on_strike+' opens the face and guides the ball to third man, easy two.', 3: '3 runs, '+on_strike+' cuts hard for a couple towards backward point. '+fielder+' from third man chases and fumbles as he picked that one lazily and throw was even more fanatic. Keeper was shouting his throat out saying that rush in quickly and throw flat.', 4: 'FOUR, flicked away and the gap is picked really well by '+on_strike+'. Bisects fine-leg and deep square. Lovely flick of the wrists.', 5: 'OUT, A searing '+bowler+' delivery finds a thick edge, and '+fielder+' tumbles to his right at a wide slip to cling onto the chance.', 6: 'SIX, Friendly half-tracker. '+on_strike+' rocks back in a trice and brutalises it over midwicket with a comprehensive pull shot. '+bowler+' watches it sail into the stands.'}

            # team scorecard updation
            total += run if run != 5 else 0
            wickets += 1 if run == 5 else 0

            # onstrike player runs updation
            run_updation(on_strike, run)

            print('\n')
            print(overs + (balls / 10), '\t', bowler + ' to ' + on_strike ,'\n')

            # to represent the time taken by bowler to run
            time.sleep(4)

            print(run if run != 5 else 'Out', '   ', comments[run])
            print('\n')

            if run % 2 == 1 and run != 5:
                on_strike, non_strike = non_strike, on_strike

            # bowler statistics update over each ball
            if run != 5:
                bowling_statistics[bowler][2] += run
            else:
                bowling_statistics[bowler][3] += 1
                if wickets <= 9:
                    on_strike = batting_order[wickets + 1][0]
                    batting_statistics[on_strike][5] = 'Not Out'
                    print(on_strike + ' came to crease')

            if balls != 6:
                n = math.floor(bowling_statistics[bowler][1])
                n += (balls / 10)
            else:
                n = math.floor(bowling_statistics[bowler][1]) + 1.0

            bowling_statistics[bowler][1] = n

            # all out case
            if wickets == 10:
                break

            # target check for 2nd innnings
            if inning == 2 and total > target:
                print('\nTarget chased...\n')
                break

        overs += 1
        last_bowler = bowler
        on_strike, non_strike = non_strike, on_strike

        # scorecard display at the end of over
        print('-'*columns)
        print('End of over ' + str(overs) + '\t\t\t' + team_name + ' ' + str(total) + ' for ' + str(wickets))
        print('\n')
        osi = batting_statistics[on_strike][6] # on strike player index
        nsi = batting_statistics[non_strike][6] # non strike player index
        print(batting[osi][1],'star ', batting_statistics[on_strike][0],'* ', batting_statistics[on_strike][1], '(',batting_statistics[on_strike][2], ')', '\t' ,
              batting[nsi][1],'star ', batting_statistics[non_strike][0],'* ', batting_statistics[non_strike][1], '(',batting_statistics[non_strike][2], ')')
        print('-'*columns)
        print('\n')

    # displaying batting scorecard and bowling scorecard
    print('\n\n', 'BATTING SCORECARD', '\n')
    print('Name'.ljust(20), 'RUNS'.ljust(20), 'BALLS'.ljust(20), 'FOURS'.ljust(20), 'SIXES'.ljust(20), 'S.R'.ljust(20))
    for i in batting_order:
        n = batting_statistics[i[0]]
        inning_bat.append(n)
        print(str(n[0]).ljust(20), str(n[1]).ljust(20), str(n[2]).ljust(20), str(n[3]).ljust(20), str(n[4]).ljust(20), str('%0.2f' %((n[1] / n[2]) * 100)).ljust(20) if (n[2] != 0) else '0.00'.ljust(20))
    print('\n')
    print('-'*columns)
    print(total, '/', wickets)
    print('-'*columns)


    print('\n\n', 'BOWLING SCORECARD', '\n')
    print('Name'.ljust(22), 'OVERS'.ljust(22), 'RUNS'.ljust(22), 'WICKETS'.ljust(22), 'ECONOMY'.ljust(22))
    for j in bowling_order:
        n = bowling_statistics[j[0]]
        inning_bowl.append(n)
        print(str(n[0]).ljust(22), str(n[1]).ljust(22), str(n[2]).ljust(22), str(n[3]).ljust(22), str('%0.2f' %(n[2] / n[1])).ljust(22) if n[1] != 0 else '0.00'.ljust(22))

    ##############################################################################################
    statistics = [inning_bat, inning_bowl]

    return (total, wickets, overs + (balls/10) if balls != 6 else overs), statistics
