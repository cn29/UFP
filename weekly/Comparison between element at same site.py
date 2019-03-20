import csv
import pprint
import matplotlib
import contextlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

def dot_prod(weekave1, weekave2):
    return np.dot(weekave1, weekave2)/(np.sqrt(np.sum(np.power(weekave1,2)) * np.sum(np.power(weekave2, 2))))

a = dot_prod([1,2,3], [4,5,6])
print(a)

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
data = []
with open('LA new.csv') as csvFile:
    readCSV = csv.reader(csvFile, delimiter=',')
    for row in readCSV:
        data.append(row)


N = len(data[0])-2                             # number of elements
elements = [Element() for _ in range(N)]        # build data container
print(N)
# iterate over all elements
for i in range(N):                              # from 0 to N-1
    print("Element ", i)
    for row in data:
        if row[1] == '' or row[i+2] == '':      # check if the data is valid
            continue
        day = int(row[1])
        value = float(row[i+2])                 #when i=16, row [17] is column 18, which is last element

        # by seasons
        date = row[0].split('/')
        # print(date)
        rem = int(date[0]) % 12              # computes the remain wrt 12
        sea_num = rem // 3                   # indicates which season is the date in
        elements[i].seasons[sea_num].weekday[day - 1].append(value)          # store Monday to Monday[0]
        elements[i].seasons[sea_num].weekday[day % 7].append(value)          # store Monday to Tuesday [1]
        elements[i].seasons[sea_num].weekday[(day+1) % 7].append(value)      # store Monday to Wednesday [2]

        # all year
        elements[i].year.weekday[day - 1].append(value)  # store the data into three days
        elements[i].year.weekday[day % 7].append(value)
        elements[i].year.weekday[(day + 1) % 7].append(value)

    # compute average & SD
    for sea_num in range(4):
        elements[i].seasons[sea_num].ave_std()
    elements[i].year.ave_std()
    elements[i].year.normalize()
    # print(elements[i].seasons[0].weekday_ave)
    # print(elements[i].seasons[0].weekSD)

# dot product
select = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
# select = range(1,17)
cov_mat = np.zeros([len(select), len(select)])
for y in range(len(select)):
    for x in range(y, len(select)):
        cov_mat[x][y] = dot_prod(elements[select[y]-1].year.weekday_ave_mmin, elements[select[x]-1].year.weekday_ave_mmin)

np.set_printoptions(precision=4)
print(cov_mat)
plt.imshow(cov_mat)
# plt.show()

# write to csv
save_csv = True
if save_csv:
    with open('LA new four seasons.csv', 'w', newline='') as target:
        wr = csv.writer(target)
        title_row = [' ', 'Winter', 'Spring', 'Summer', 'Fall', 'Annual']
        wr.writerow(title_row)
        for i in range(N):
            row = elements[i].season_sd()
            row.insert(0, i)
            row.append(elements[i].year.weekSD)
            wr.writerow(row)


# write to csv2
if save_csv:
    with open('LA new covmat.csv', 'w', newline='') as target:
        wr = csv.writer(target)
        title_row = list(range(1,len(select)+1))
        title_row.insert(0, '')
        wr.writerow(title_row)
        for i in range(len(select)):
            row = cov_mat[i]
            print(row)
            np.insert(row, 0, float(i+1))
            print(row)
            wr.writerow(row)