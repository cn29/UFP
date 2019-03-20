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
    week_group = []
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
    return week_group, data_3day, mean_3day


if __name__ == "__main__":
    # set print format
    float_formatter = lambda x: "%.3f" % x
    np.set_printoptions(formatter={'float_kind': float_formatter})
    num_weeks = 50


    means_x = np.asarray([35.5123, 44.3578, 48.0436, 43.5154, 34.7159, 28.6967, 29.7039])
    sigma_x = np.asarray([30]*7)
    means = np.log(means_x/np.sqrt(1+np.square(sigma_x)/np.square(means_x)))
    sigma = np.sqrt(np.log(1+np.square(sigma_x)/np.square(means_x)))
    week_data = week_simulate(means, sigma, num_weeks)
    # compute mean of each day in a week
    mean_original = np.mean(week_data, axis=1)
    print("Sample mean for each day in a week: \n\t", mean_original)
    # flatten (2d -> 1d): from [7, weeks] to [7*weeks]
    week_data = week_data.flatten('F')
    # re-sample, 3 continues days
    print("Re-sample data by a group of 3 continues days....")

    week_group, data_3day, mean_3day = resample(week_data, num_weeks)
    imin = 0
    imax = 0
    for i in range (7):
        if mean_3day[i] < mean_3day[imin]:
            imin = i
        if mean_3day[i] > mean_3day[imax]:
            imax = i
    [_,pvalue] = stats.ttest_ind(week_group[imin],week_group[imax], equal_var=False)
    print("Original means: \n\t", mean_original)
    print("Resampled means: \n\t", mean_3day)
    print("p value is: ", pvalue)
    print("min group:", week_group[imin])
    print('max group:', week_group[imax])
    # draw
    plt.plot(range(7), mean_original, '-o')
    plt.plot(range(7), mean_3day, '-o')
    plt.legend(['original', '3day re-sample'])
    plt.show()

    print(sigma)