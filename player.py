import random

f_Names = {0: 'Kalyan',
              1: 'Akash',
              2: 'Mahesh',
              3: 'Abhi',
              4: 'Gopi',
              5: 'Srinu',
              6: 'Charan',
              7: 'Siddhu',
              8: 'Teja',
              9: 'Sathish',
              10: 'Sai',
              11: 'Ajay',
              12: 'Subbu',
              13: 'Dhruv',
              14: 'Chand',
              15: 'Sagar',
              16: 'Praveen',
              17: 'Yugam',
              18: 'Atul',
              19: 'Arun',
              20: 'Sandeep',
              21: 'Sekhar',
              22: 'Krish',
              23: 'Prabhas',
              24: 'Arjun',
              25: 'Devansh'}

l_Names = {0: 'Eti',
              1: 'Palnati',
              2: 'Kommu',
              3: 'Lanka',
              4: 'Thota',
              5: 'Siddha',
              6: 'Yelem',
              7: 'Yerramsetti',
              8: 'Kuncha',
              9: 'kunchaala',
              10: 'Uppalapaati',
              11: 'Munagala',
              12: 'Mopidevi',
              13: 'Midathala',
              14: 'Janjam',
              15: 'Junjunnuru',
              16: 'Konidela',
              17: 'Nandamuri',
              18: 'Rao',
              19: 'Nara',
              20: 'Pasupuleti',
              21: 'Kumbhampati',
              22: 'Ghattamaneni',
              23: 'Allu',
              24: 'Botsha',
              25: 'Ravuru'}


class Player:

    def generate(self):
        name = f_Names[random.randint(0,25)] + ' ' + l_Names[random.randint(0,25)].capitalize()
        return [name,
                random.randint(0,20),
                random.randint(0,20),
                random.randint(0,20),
                random.randint(0,20),
                random.randint(0,20),
                random.randint(0,20)]


# for testing, uncomment the below  line
# print(Player().generate())


