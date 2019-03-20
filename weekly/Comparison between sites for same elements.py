import csv
import pprint
import matplotlib
import contextlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

def dot_prod(weekave1, weekave2):
    return np.dot(weekave1, weekave2)/(np.sqrt(np.sum(np.power(weekave1,2)) * np.sum(np.power(weekave2, 2))))


# a collection of weekly stored data
class WeekData:
    def __init__(self):                                #set initial values
        self.weekday = [[] for _ in range(7)]
        self.weekday_ave = []
        self.weekSD = 1.1
        self.weekday_ave_mmin = [[] for _ in range(7)]

    def ave_std(self):                                 #write functions
        self.weekday_ave = [float(sum(l)) / len(l) for l in self.weekday]           #computes average of weekdays
        self.weekSD = np.std(self.weekday_ave)/np.mean(self.weekday_ave)            #computes std dev of weekdays

    def normalize(self):
        self.weekday_ave_mmin = self.weekday_ave - np.min(self.weekday_ave)


class Element:
    def __init__(self):
        self.seasons = [WeekData() for _ in range(4)]
        self.year = WeekData()

    def season_sd(self):
        return [self.seasons[i].weekSD for i in range(4)]                       #return std dev of weekdays in each season


# read data from csv
dataSP = []
with open('SP new_ave.csv') as csvFile:
    readCSV = csv.reader(csvFile, delimiter=',')
    for row in readCSV:
        dataSP.append(row)

dataEO =[]
with open('EO new_ave.csv') as csvFile:
    readCSV = csv.reader(csvFile, delimiter=',')
    for row in readCSV:
        dataEO.append(row)

dataLA = []
with open('LA new_ave.csv') as csvFile:
    readCSV = csv.reader(csvFile, delimiter=',')
    for row in readCSV:
        dataLA.append(row)

dataFresno = []
with open('FN new_ave.csv') as csvFile:
    readCSV = csv.reader(csvFile, delimiter=',')
    for row in readCSV:
        dataFresno.append(row)

site = [Element() for _ in range(4)]
ele =  11
site[0].year.weekday_ave = list(map(float, dataSP[ele]))
site[1].year.weekday_ave = list(map(float, dataEO[ele]))
site[2].year.weekday_ave = list(map(float, dataLA[ele]))
site[3].year.weekday_ave = list(map(float, dataFresno[ele]))
for i in range(4):
    site[i].year.normalize()   #compute


# dot product
cov_mat = np.zeros([4, 4])
for y in range(4):
    for x in range(y, 4):
        cov_mat[x][y] = dot_prod(site[y].year.weekday_ave_mmin, site[x].year.weekday_ave_mmin) #return

np.set_printoptions(precision=4)
print(cov_mat)
plt.imshow(cov_mat)
# plt.show()

# write to csv2
save_csv = True
if save_csv:
    with open('Site_covmat.csv', 'w', newline='') as target:
        wr = csv.writer(target)
        title_row = list(range(1,4+1))
        title_row.insert(0, '')
        wr.writerow(title_row)
        for i in range(4):
            row = cov_mat[i]

            np.insert(row, 0, float(i+1))

            wr.writerow(row)