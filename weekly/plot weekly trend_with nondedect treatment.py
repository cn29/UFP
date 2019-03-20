import csv
import matplotlib.pyplot as plt
import numpy as np

# read data from csv
data = []
with open('FN new split.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    i = 0
    for row in readCSV:
        data_row = []
        for element in row:
            data_row.append(element)

        data.append(data_row)
        i = i + 1

elem_name = data[0][:]
thres1 =  data[1][:]
thres2 = data[2][:]
print(thres1)
print(thres2)

N = len(data[0])-2
# compute average
week_ave = []
fig = plt.figure()
ax = [None for _ in range(1, 17)]
for i in range(1,17):
    weekday = []
    for k in range(1,8):
        weekday.append([])
    j = 0
    # starts from 4th row in data
    for ii in range(3, len(data)):
        row = data[ii]
        if row[1] == '' or row[i+1] == '':
            continue
        day = int(row[1])
        value = float(row[i+1])
        # ---------  threshold preprocessing -----------
        print(value, float(thres1[i+1]))
        #if(value < float(thres1[i+1])):
        #    value = float(thres1[i+1])/2
        #    data[ii][i+1] = value
        # ----------------------------------------------
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
        #print("%.7f" % stats[1], end="\t")d
        #print("%.7f" % stats[2])
        average.append(sum(row)/len(row))
        counter += 1
        summary_stats.append(stats)
    # ----- plot -----
    if 1: #= 2:
        ax[i-1] = fig.add_subplot(4,4,i)
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
        print(norm_means)
        print(errors)

        x = list(range(1, 8))
        objects=('Mon','Tue','Wed','Thu','Fri','Sat','Sun')
        y_pos=np.arange(len(objects))
        ax[i-1].bar(y_pos,norm_means, width=0.6,color='red', yerr=errors, alpha=0.5,
                error_kw=dict(ecolor='gray',lw=2,capsize=5,capthick=2))
        #ax[i - 1].xticks(y_pos,objects)
        #ax[i - 1].yticks(np.arange(0,1.501,0.5))
        ax[i - 1].plot(np.arange(-1,8,1), np.ones([9,1]), '--', color='gray')
        ax[i - 1].axis((-0.9, 6.9, 0, 2))
        # xtick ytick
        ax[i-1].set_xticks(range(7))
        ax[i-1].set_xticklabels(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
        for tick in ax[i-1].xaxis.get_major_ticks():
            tick.label.set_fontsize(13)
        for tick in ax[i-1].yaxis.get_major_ticks():
            tick.label.set_fontsize(13)
        title_str = elem_name[i+1] + '  Mean=' + '{:.4f}'.format(a_mean) + ' ng/m$^3$'
        #ax[i - 1].title(fontdict=fontdict).set_text(elem_name[i+1])
        ax[i-1].set_title(title_str,fontdict={'fontsize': 18})
        # plt.errorbar(objects,norm_means,errors,xerr=None)
#fig.tight_layout()
#fig.savefig('temp.png', dpi=400)
plt.subplots_adjust(hspace=0.4)
plt.show()

# write to cs
#save_csv = True
#if save_csv:
#    with open('LA_half DL.csv', 'w', newline='') as target:
#        wr = csv.writer(target)
#        for row in data:
#            wr.writerow(row)





