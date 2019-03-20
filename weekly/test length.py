import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# read data from csv
data = []
with open('test length of sampling.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',') #extract data from csv file
    i = 0
    for row in readCSV:
        data_row = []                           #write rows in readCSV to data_row
        for element in row:
            data_row.append(element)            #append data in row to data_row

        data.append(data_row)                   #append data_row to data
        i = i + 1

#N = len(data[0])-2                              #count number of elements
# compute average
week_ave = []
week_std = []
pvalue_list = []
for i in range(1,2):                           #for every element, there is one weekday list
    weekday = []
    for k in range(1,8):                        #weekday has 7 values
        weekday.append([])
    for ii in range(3, len(data)):              #len(data) is the total number of rows
        row = data[ii]                          #ii denotes the index of row
        #if row[1] == '' or row[i+1] == '':      #skip if the day of week is blank or the concentration is blank
        #    continue
        day = int(row[1])
        value = float(row[i+1])
        weekday[day - 1].append(value)           #append value to the day, the day after the day and two days after the day
        weekday[day % 7].append(value)
        weekday[(day+1) % 7].append(value)

    average = []                                #average and std are list
    std = []
    for row in weekday:                         #weekday has seven rows
        average.append(sum(row)/len(row))       #calculate the average of each row in weekday, average contains seven values for one element
        std.append(np.std(row))                 #calcualte the std dev of each row in weekday
    week_ave.append(average)                    #week_ave contains seven values
    week_std.append(std)
    #t test for max and min in a week
    w_min = 0
    w_max = 0
    for j in range(0,7):
        if average[j] < average[w_min]:         #w_min is the index in average that has min value
            w_min = j
        if average[j] > average[w_max]:         #w_max is the index that has max value
            w_max = j
    wmin_group = weekday[w_min]                 #wmin_group is the min value in the seven values of weekday
    wmax_group = weekday[w_max]                 #wmax_group is the max value in the seven values of weekday
    [_, pvalue] = stats.ttest_ind(wmin_group, wmax_group, equal_var = False)
    pvalue_list.append(pvalue)                  #there is one p value for one element
    #if i == 15:
    #    print(wmin_group)
    #    print(wmax_group)

print(pvalue_list)

#week = list(range(1, 8))
#plt.plot(week, average)
#plt.show()

# write to csv
save_csv = True
if save_csv:
    with open('test length', 'w', newline='') as target:
        wr = csv.writer(target)
        for row in week_ave:
            wr.writerow(row)
        for row in week_std:
            wr.writerow(row)

