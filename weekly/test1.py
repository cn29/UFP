import csv
#import matplotlib.pyplot as plt
import numpy as np

# read data from csv
data = []
with open('D:/Wei/Research/python3/project1/data/LA+S.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    i = 0
    for row in readCSV:
        data_row = []
        for element in row:
            data_row.append(element)

        data.append(data_row)
        i = i + 1

N = len(data[0])-2
# compute average
week_ave = []
for i in range(1,17):
    weekday = []
    for k in range(1,8):
        weekday.append([])
    j = 0
    for row in data:
        if row[1] == '' or row[i+1] == '':
            continue
        day = int(row[1])
        value = float(row[i+1])
        weekday[day - 1].append(value)
        weekday[day % 7].append(value)
        weekday[(day+1) % 7].append(value)

    average = []
    for row in weekday:
        average.append(sum(row)/len(row))
    week_ave.append(average)

print(week_ave)
#plotave = False
#if plotave:
#    week = list(range(1, 8))
#    plt.plot(week)
#    plt.show()

# write to cs
save_csv = True
if save_csv:
    with open('D:/Wei/Research/python3/project1/data/LA+S_ave.csv', 'w') as target:
        wr = csv.writer(target)
        for row in week_ave:
            wr.writerow(row)
