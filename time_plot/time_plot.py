import matplotlib.pyplot as plt
import csv
from datetime import datetime

plt.rcParams["font.family"] = "Times New Roman"


def load_data(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        tickers = []
        data_matrix = []
        source_name = []
        for row in csv_reader:
            if line_count == 0:
                # read source name on 1st row
                source_name = row[1:]
                print(source_name)
            else:
                tickers.append(row[0])
                for i in range(1,len(row)):
                    if line_count == 1:
                        data_matrix.append([])
                    data_matrix[i-1].append(float(row[i]))

            line_count += 1
        return tickers, data_matrix, line_count-1, source_name


if __name__ == '__main__':
    # load data
    option = 1
    file_name = ''

    if option == 1:
        file_name = 'TimeSeries_SP.csv'
        figure_title = 'San Pablo'
    elif option == 2:
        file_name = 'TimeSeries_EO.csv'
        figure_title = 'East Oakland'
    elif option == 3:
        file_name = 'TimeSeries_LA.csv'
        figure_title = 'Los Angeles'


    dates, data_matrix, line_count, source_name = load_data(file_name)

    print(dates)
    x_index = []
    x_index.append(1)
    start_date_obj = datetime.strptime(dates[0], '%m/%d/%Y')
    dates = dates[1:]
    for date in dates:
        date_obj1 = datetime.strptime(date, '%m/%d/%Y')
        delta = date_obj1 - start_date_obj
        x_index.append(delta.days+1)

    print(x_index)

    # plot
    y_label = 'Concentration $(ng/m^3)$'
    # ticks = ['Aug 2015', 'Sep 2015', 'Oct 2015', 'Nov 2015', 'Dec 2015', 'Jan 2016', 'Feb 2016', 'Mar 2016', 'Apr 2016', 'Mar 2016', 'Jun 2016']
    ticks = ['2015\n   Aug', 'Sep', 'Oct', 'Nov', 'Dec', '2016\n   Jan', 'Feb', 'Mar', 'Apr',
             'Mar', 'Jun']
    tick_pos = [1+x*30 for x in range(12)]
    num_plots = len(data_matrix)
    f, axarr = plt.subplots(num_plots, sharex=True, sharey=False)
    f.text(0.04, 0.5, y_label, va='center', rotation='vertical', fontsize=14)
    f.suptitle(figure_title)
    ax2 = []

    for i in range(num_plots):
        l1 = axarr[i].plot(x_index, data_matrix[i], alpha=0.85, color='black')
        print(max(data_matrix[i]))

    for i in range(num_plots):
        axarr[i].set_xticks(tick_pos)
        axarr[i].set_xticklabels(ticks)
        # axarr[i].set_yscale('log')
        axarr[i].yaxis.set_tick_params(labelsize=11)
        axarr[i].xaxis.set_tick_params(rotation=45, labelsize=11)
        axarr[i].set_ylim([0, int(max(data_matrix[i]))])
        # source caption
        axarr[i].text(0.95, 0.9, source_name[i],
                      verticalalignment='top', horizontalalignment='right',
                      transform=axarr[i].transAxes,
                      color='black', fontsize=11)

        # plot percent matirx
        # if percent_matrix != []:
        #     print(percent_matrix[i])
        #     ax2.append(axarr[i].twinx())
        #     s2 = percent_matrix[i]
        #     l2, = ax2[i].plot(x, s2, 'rh', alpha=0.6, markersize=4)
        #     # ax2[i].tick_params('y', colors='r')
        #     ax2[i].set_ylim(0, 100)

        if i == 0:
            axarr[i].xaxis.set_tick_params(labeltop='on')

    # plt.ylim((10 ** -1, 10 ** 3))
    # f.legend((l1, l2), ('Concentration', 'Percentage'), 'upper right')
    # f.legend((l1), ('Concentration'), 'upper right')
    plt.show()

