
from player import Player

class teams:
    def __init__(self):
        self.team1 = []
        self.team2 = []

    def generate_team(self):
        players = []
        while len(self.team1) < 11:
            player = Player().generate()
            if player[0] not in players:
                self.team1.append(player)
                players.append(player[0])
        while len(self.team2) < 11:
            player = Player().generate()
            if player[0] not in players:
                self.team2.append(player)
                players.append(player[0])

        return self.team1, self.team2


# for testing,uncomment the below 3 lines


# t = teams()
# sandeep, akash = t.generate_team()
# print(*sandeep, sep='\n\n')
