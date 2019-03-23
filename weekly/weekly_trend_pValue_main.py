import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import datetime


def truncate_data(weekday):
    # truncate data to same size
    sum_col = np.sum(weekday, axis=0)
    weekday2 = weekday
    for i in range(52):
        ind = 51 - i
        if sum_col[ind] == -7:
            weekday2 = np.delete(weekday2, ind, 1)
    return weekday2


if __name__ == '__main__':
    # read data from csv
    dir_name = './data_files/'
    option = 1
    file_name = ''

    if option == 1:
        file_name = dir_name+'LA_new_split.csv'


    data = []
    with open(file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in readCSV:
            data_row = []
            for element in row:
                data_row.append(element)

            data.append(data_row)
            i = i + 1

    elem_name = data[0][2:]
    num_plots = len(data[0]) - 2
    # compute average
    pValue_list = []
    fig = plt.figure()
    ax = [None for _ in range(1, num_plots+1)]

    start_obj = datetime.datetime.strptime(data[3][0], "%m/%d/%Y")

    for i in range(1, num_plots+1):
        # Initialize weekday as 7*52, filled with -1
        weekday = np.full((7,52), -1.0)

        # starts from 4th row in data
        for ii in range(3, len(data)):
            row = data[ii]
            if row[1] == '' or row[i+1] == '':
                continue
            date_obj = datetime.datetime.strptime(row[0], "%m/%d/%Y")
            day_of_week = int(row[1]) - 1
            for d in range(3):
                delta = date_obj - start_obj + datetime.timedelta(days=d)
                n_week = int(delta.days/7)
                day_of_week_now = (day_of_week+d)%7
                weekday[day_of_week_now][n_week] = float(row[i + 1])

            # ---------  threshold pre-processing -----------
            # print(value, float(thres1[i+1]))
            # if(value < float(thres1[i+1])):
            #    value = float(thres1[i+1])/2
            #    data[ii][i+1] = value
            # ----------------------------------------------

        # post-processing
        weekday = truncate_data(weekday)

        # get mean and std
        means = []
        counter = 1
        summary_stats = []
        for day in range(7):
            row = weekday[day]
            L = len(row)
            for k in range(L):
                if row[L-k-1] == -1:
                    row = np.delete(row, L-k-1)

            mean = np.mean(row)
            std = np.std(row)
            means.append(mean)
            counter += 1
            summary_stats.append([len(row), mean, std])


        # paired t test for max and min in a week
        w_min = 0
        w_max = 0
        for j in range(7):
            if means[j] < means[w_min]:
                w_min = j
            elif means[j] > means[w_max]:
                w_max = j
        wmin_group = weekday[w_min]
        wmax_group = weekday[w_max]
        L = len(wmax_group)
        for j in range(L):
            ind = L-1-j
            if wmax_group[ind] < 0 or wmin_group[ind] < 0:
                wmax_group = np.delete(wmax_group, ind)
                wmin_group = np.delete(wmin_group, ind)
        [_, pValue] = stats.ttest_rel(wmin_group, wmax_group, nan_policy='omit')
        pValue_list.append(pValue)

        # ----- plot wmin & wmax ------
        if 0:
            plt.figure()
            plt.plot(wmin_group)
            plt.plot(wmax_group)
            plt.title('{} pValue={:.3f}'.format(elem_name[i-1], pValue))
            plt.legend(['min={:.2f}'.format(min(means)),'max={:.2f}'.format(max(means))])
            plt.show()

        # ----- plot means -----
        if 1: #= 2:
            ax[i-1] = fig.add_subplot(4,4,i)
            a_sum = 0
            a_num = 0
            for idx in range(7):
                a_sum +=summary_stats[idx][0]*summary_stats[idx][1]
                a_num += summary_stats[idx][0]
            a_mean = a_sum/a_num
            norm_means = []
            errors = []
            for idx in range(0,7):
                norm_means.append(summary_stats[idx][1]/a_mean)
                errors.append(summary_stats[idx][2]/np.sqrt(summary_stats[idx][0])/a_mean)
            # print(norm_means)
            # print(errors)

            x = list(range(1, 8))
            objects=('Mon','Tue','Wed','Thu','Fri','Sat','Sun')
            y_pos=np.arange(len(objects))
            ax[i-1].bar(y_pos,norm_means, width=0.6,color='black', yerr=errors, alpha=0.3,
                    error_kw=dict(ecolor='gray',lw=2,capsize=6,capthick=2))
            #ax[i - 1].xticks(y_pos,objects)
            #ax[i - 1].yticks(np.arange(0,1.501,0.5))
            ax[i - 1].plot(np.arange(-1,8,1), np.ones([9,1]), ':', color='gray')
            # ax[i - 1].axis((-0.9, 6.9, 0, 3))
            # xtick ytick
            ax[i-1].set_xticks(range(7))
            ax[i-1].set_xticklabels(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
            for tick in ax[i-1].xaxis.get_major_ticks():
                tick.label.set_fontsize(13)
            for tick in ax[i-1].yaxis.get_major_ticks():
                tick.label.set_fontsize(13)
            title_str = elem_name[i-1] + '  Mean=' + '{:.3f}'.format(a_mean) + ' ng/m$^3$'
            #ax[i - 1].title(fontdict=fontdict).set_text(elem_name[i+1])
            ax[i-1].set_title(title_str,fontdict={'fontsize': 16})
            # plt.errorbar(objects,norm_means,errors,xerr=None)

    #fig.tight_layout()
    #fig.savefig('temp.png', dpi=400)
    plt.subplots_adjust(hspace=0.4)
    plt.show()
    print('-------- print p values --------')
    attach_sign = ''
    for j in range(len(elem_name)):
        attach_sign = '*' if pValue_list[j] < 0.05 else ''
        line = '{}\t: {:3f} {}'.format(elem_name[j], pValue_list[j], attach_sign)
        print(line)

    # write to cs
    #save_csv = True
    #if save_csv:
    #    with open('LA_half DL.csv', 'w', newline='') as target:
    #        wr = csv.writer(target)
    #        for row in data:
    #            wr.writerow(row)





