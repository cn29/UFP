import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


if __name__ == '__main__':
    # read data from csv
    data = []
    file_name = 'SP new split.csv'

    with open(file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',') #extract data from csv file
        i = 0
        for row in readCSV:
            data_row = []
            for element in row:
                data_row.append(element)

            data.append(data_row)
            i = i + 1

    num_plots = len(data[0])-2
    # compute average
    week_ave = []
    week_std = []
    pvalue_list = []
    for i in range(1,num_plots+1):
        weekday = []
        for k in range(1,8):
            weekday.append([])
        for ii in range(3, len(data)):              #len(data) is the total number of rows
            row = data[ii]
            if row[1] == '' or row[i+1] == '':
                continue
            day = int(row[1])
            value = float(row[i+1])
            weekday[day - 1].append(value)
            weekday[day % 7].append(value)
            weekday[(day+1) % 7].append(value)

        average = []
        std = []
        for row in weekday:
            average.append(sum(row)/len(row))
            std.append(np.std(row))
        week_ave.append(average)
        week_std.append(std)
        #t test for max and min in a week
        w_min = 0
        w_max = 0
        for j in range(0,7):
            if average[j] < average[w_min]:
                w_min = j
            if average[j] > average[w_max]:
                w_max = j
        wmin_group = weekday[w_min]
        wmax_group = weekday[w_max]
        [_, pvalue] = stats.ttest_rel(wmin_group, wmax_group, nan_policy ='omit')
        pvalue_list.append(pvalue)
        if i == 15:
            print(wmin_group)
            print(wmax_group)

    print(pvalue_list)

    #week = list(range(1, 8))
    #plt.plot(week, average)
    #plt.show()

    # write to csv
    save_csv = True
    if save_csv:
        with open('SP new ave_std', 'w', newline='') as target:
            wr = csv.writer(target)
            for row in week_ave:
                wr.writerow(row)
            for row in week_std:
                wr.writerow(row)
