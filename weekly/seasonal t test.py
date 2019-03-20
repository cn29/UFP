import csv
import pprint
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


# a collection of weekly stored data
class WeekData:
    def __init__(self):                                #set initial values
        self.weekday = [[] for _ in range(7)]
        self.weekday_ave = []
        self.weekSD = 1.1

    def ave_std(self):                                 #write functions
        self.weekday_ave = [float(sum(l)) / len(l) for l in self.weekday]           #computes average of weekdays
        self.weekSD = np.std(self.weekday_ave)/np.mean(self.weekday_ave)            #computes std dev of weekdays


class Element:
    def __init__(self):
        self.seasons = [WeekData() for _ in range(4)]
        self.year = WeekData()

    def season_sd(self):
        return [self.seasons[i].weekSD for i in range(4)]                       #return std dev of weekdays in each season


# read data from csv
data = []
with open('FN new.csv') as csvFile:
    readCSV = csv.reader(csvFile, delimiter=',')
    for row in readCSV:
        data.append(row)


N = len(data[0])-2                             # number of elements
elements = [Element() for _ in range(N)]  # build data container

# iterate over all elements
for i in range(N):                              # from 0 to N-1
    for row in data:
        if row[1] == '' or row[i+2] == '':      # check if the data is valid
            continue
        day = int(row[1])
        value = float(row[i+2])                 #when i=16, row [17] is column 18, which is last element

        # by seasons
        date = row[0].split('/')
        # print(date)
        rem = int(date[0]) % 12              # computes the remain wrt 12
        sea_num = rem // 3                   # indicates which season is the date ind
        elements[i].seasons[sea_num].weekday[day - 1].append(value)          # store Monday to Monday[0]
        elements[i].seasons[sea_num].weekday[day % 7].append(value)          # store Monday to Tuesday [1]
        elements[i].seasons[sea_num].weekday[(day+1) % 7].append(value)      # store Monday to Wednesday [2]

        # all year
        elements[i].year.weekday[day - 1].append(value)  # store the data into three days
        elements[i].year.weekday[day % 7].append(value)
        elements[i].year.weekday[(day + 1) % 7].append(value)

    # compute average
    pvalue_list = []
    for sea_num in range (4):
        if sea_num == 1 or sea_num == 3:
            continue
        w_min = 0
        w_max = 0

        elements[i].seasons[sea_num].ave_std()
        for j in range(0,7):
            if elements[i].seasons[sea_num].weekday_ave[j] < elements[i].seasons[sea_num].weekday_ave[w_min]:
                w_min = j
            if elements[i].seasons[sea_num].weekday_ave[j] > elements[i].seasons[sea_num].weekday_ave[w_max]:
                w_max = j
        wmin_group =  elements[i].seasons[sea_num].weekday[w_min]
        wmax_group =  elements[i].seasons[sea_num].weekday[w_max]
        [_, p_value] = stats.ttest_ind(wmin_group, wmax_group, equal_var = False)
        pvalue_list.append(p_value)
    print(pvalue_list)
