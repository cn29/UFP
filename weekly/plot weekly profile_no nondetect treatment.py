import csv
import matplotlib.pyplot as plt
import numpy as np

# read data from csv
data = []
with open('C:/Users/weixu/Google Drive/Wei/Research/python3/project1/data/EO-spring.csv') as csvfile:
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
    # post-processing

    average = []
    counter = 1
    summary_stats = []
    for row in weekday:
        stats = []
        stats.append(len(row))
        stats.append(np.mean(row))
        stats.append(np.std(row))
        #print(counter, end="\t")
        #print(stats[0], end="\t")
        #print("%.7f" % stats[1], end="\t")
        #print("%.7f" % stats[2])
        average.append(sum(row)/len(row))
        counter += 1
        summary_stats.append(stats)
    if i == 16:
        a_sum = 0
        a_num = 0
        for idx in range(0,7):
            a_sum +=summary_stats[idx][0]*summary_stats[idx][1]
            a_num += summary_stats[idx][0]
        a_mean = a_sum/a_num
        norm_means = []
        errors = []
        for idx in range(0,7):
            norm_means.append(summary_stats[idx][1]/a_mean)
            errors.append(summary_stats[idx][2]/np.sqrt(summary_stats[idx][0])/a_mean)
        print(a_mean)


        x = list(range(1, 8))
        objects=('Mon','Tue','Wed','Thu','Fri','Sat','Sun')
        y_pos=np.arange(len(objects))
        plt.bar(y_pos,norm_means, width=0.6,color='red', yerr=errors, alpha=0.5,
                error_kw=dict(ecolor='gray',lw=2,capsize=5,capthick=2))
        plt.xticks(y_pos,objects)
        plt.yticks(np.arange(0,4.5,0.5))
        plt.plot(np.arange(-1,8,1), np.ones([9,1]), '--', color='gray')
        plt.axis((-1,7,0,3))
        # plt.errorbar(objects,norm_means,errors,xerr=None)
        plt.show()




#print(week_ave)
#plotave = False
#if plotave:
#    week = list(range(1, 8))
#    plt.plot(week)
#    plt.show()

# write to cs
#save_csv = True
#if save_csv:
#    with open('D:/Wei/Research/python3/project1/data/LA+S_weekday.csv', 'w') as target:
#        wr = csv.writer(target)

