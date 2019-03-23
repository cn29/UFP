import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def week_simulate(means, sigma, weeks):                                 #simulates the real concentration
    week_data = np.empty([7, weeks])                                   #rows=7, columns=number of weeks
    for i in range(7):                                                 #for each row (each day of week), generate some numbers that has same mean and vars
        week_data[i] = np.random.lognormal(means[i], sigma[i], weeks)
    return week_data


def resample(week_data, weeks):
    size_new = int(7*weeks/3)                                          #number of 3-day samples
    data_3day = np.ones([size_new*3])                                  #initialize the resampled days, data_3day has only one row, one week after another
    for i in range(size_new):
        ii = i*3
        average = (week_data[ii] + week_data[ii+1] + week_data[ii+2])/3 #calculate the 3-day mean
        #print(ii, week_data[ii], week_data[ii+1] , week_data[ii+2], average)
        data_3day[ii] = average                                         #append 3-day means to the 3 days it covers
        data_3day[ii+1] = average
        data_3day[ii+2] = average
    # compute mean of each day in a week
    week_group = []                                                     #arrange the one-line data_3day to a matrix
    #print (week_group)
    mean_3day = np.zeros([7])
    mean_count = np.zeros([7])
    for i in range(7):                                                 #cycle in the seven days of a week
        week_group.append([])                                          #set a new space for new numbers appended
        #print (week_group)
        for j in range(size_new):                                      #cycle in the number of 3 day sample
            if (i+j*7 < len(data_3day)):
                week_group[i].append(data_3day[i+j*7])                     #add all the mondays, tue...for each i
                mean_count[i] += 1
                mean_3day[i] += data_3day[i+j*7]
            else:
                break
    mean_3day /= mean_count
    return week_group, data_3day, mean_3day                             #week_group:matrix of resampled data,
                                                                        #data_3day: a line of resampled data
                                                                        #mean_3day: seven numbers of mean for each day
def get_week_ave(means, sigma, num_weeks):
    week_data = week_simulate(means, sigma, num_weeks)
    # compute mean of each day for generated data
    mean_test = np.mean(week_data, axis=1)
    # print("Sample mean for each day in a week: \n\t", mean_test)
    # flatten (2d -> 1d): from [7, weeks] to [7*weeks]
    week_data = week_data.flatten('F')
    # re-sample, 3 continues days
    # print("Re-sample data by a group of 3 continues days....")
    week_group, data_3day, mean_test_3day = resample(week_data, num_weeks) #?

    #count elements in each day in week_group, find min
    num_element = np.zeros(7)
    min_num_element = 0
    for i in range(7):
        num_element[i] = len(week_group[i])

    min_num_elememt = min(num_element)
    #print(min_num_elememt)

    week_group2 = np.zeros([7,int(min_num_elememt)])                           #week_group2: week_group in array format
    for i in range(7):
        for j in range(int(min_num_elememt)):
            week_group2[i,j] = week_group[i][j]

    imin = 0
    imax = 0
    for i in range(7):
        if mean_test_3day[i] < mean_test_3day[imin]:
            imin = i
        if mean_test_3day[i] > mean_test_3day[imax]:
            imax = i

    #print(imax, imin, len(week_group[imin]),len(week_group[imax]))
    [_, pvalue] = stats.ttest_rel(week_group2[imin], week_group2[imax])
    #print('p value is', pvalue)

    return mean_test_3day, mean_test, pvalue                            #mean_test_3day: seven mean for resampled data
                                                                        #mean_test: seven mean for generated data
                                                                        #pvalue: p value for one set of experiment


if __name__ == "__main__":
    # set print format
    float_formatter = lambda x: "%.3f" % x
    np.set_printoptions(formatter={'float_kind': float_formatter})
    num_weeks = [5,10,20,30,50,100]
    repeat = [30]
    means_x = np.asarray([35.5123, 44.3578, 48.0436, 43.5154, 34.7159, 28.6967, 29.7039])
    sigma_x = np.asarray([35.5123, 44.3578, 48.0436, 43.5154, 34.7159, 28.6967, 29.7039])
    sigma_x = 0.7*sigma_x
    means = np.log(means_x/np.sqrt(1+np.square(sigma_x)/np.square(means_x)))
    sigma = np.sqrt(np.log(1+np.square(sigma_x)/np.square(means_x)))




    # plot
    fig, axes = plt.subplots(2, int(len(num_weeks)/2))

    mean_3day_arr = np.zeros([len(num_weeks), 7])
    std_3day_arr = np.zeros([len(num_weeks), 7])

    for x in range(0, len(repeat)):
        for y in range(0, len(num_weeks)):
            mean_data = np.zeros([7, repeat[x]])
            mean_data_3day = np.zeros([7, repeat[x]])
            pvalue_group = np.zeros(repeat[0])
            for i in range(repeat[x]):
                n = num_weeks[y]
                mean_test_3day, mean_test, pvalue = get_week_ave(means, sigma, n)

                pvalue_group[i] = pvalue
                for w in range(7):
                    mean_data[w, i] = mean_test[w]                                      #append data in mean_test to mean_data
                    mean_data_3day[w, i] = mean_test_3day[w]


            mean_mean_data = mean_data.mean(axis=1)
            std_mean_data = mean_data.std(axis=1)
            mean_mean_data_3day = mean_data_3day.mean(axis=1)
            std_mean_data_3day = mean_data_3day.std(axis=1)
            mean_pvalue = pvalue_group.mean()
            print('The mean p value for',num_weeks[y],'weeks is', mean_pvalue)
            print('The day-of-week concentrations for 3-day are\n', mean_mean_data_3day)

            x1 = int((y)/3)
            x2 = y%3
            a = axes[x1, x2].errorbar(range(7), means_x, yerr=std_mean_data, color='black',
                                      fmt='-o', capsize=4, linestyle=':', alpha=0.5)
            a[-1][0].set_linestyle(':')
            if x2 == 0:
                axes[x1, x2].set_ylabel('ng/m$^3$')

            axes[x1, x2].errorbar(range(7), mean_mean_data_3day, yerr=std_mean_data_3day, color='black',
                                  fmt='-o', capsize=4)
            axes[x1, x2].legend(['A=True', 'B=3-day average'])
            title_string = 'num of weeks={}\npvalue={:.4f}'.format(num_weeks[y],mean_pvalue)
            axes[x1, x2].set_title(title_string, va='bottom')
            axes[x1, x2].set_ylim([10,65])
            axes[x1, x2].set_xticks(range(7))
            axes[x1, x2].set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
            for tick in axes[x1, x2].xaxis.get_major_ticks():
                tick.label.set_fontsize(11)
            mean_3day_arr[y] = mean_mean_data_3day
            std_3day_arr[y] = std_mean_data_3day

    # plt.plot(range(7), mean_test, '-o')
    # plt.plot(range(7), mean_test_3day, '-o')
    # plt.legend(['original', '3day re-sample'])
    if 0:
        plt.figure(2)
        for i in range(len(num_weeks)):
            plt.errorbar(range(7), mean_3day_arr[i], yerr=std_3day_arr[i], fmt='-o', capsize=4)

        plt.legend(num_weeks)

    plt.subplots_adjust(top = 0.88,
                        bottom = 0.11,
                        left = 0.11,
                        right = 0.9,
                        hspace = 0.29,
                        wspace = 0.2)


    plt.show()
