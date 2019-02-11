import matplotlib.pyplot as plt
import numpy as np
import csv

from repo_config import *


def load_data(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        tickers = []
        data_matrix = []
        source_name = []
        for row in csv_reader:
            if row[0] == 'source' or '':
                # read source name on 1st row
                source_name = row[1:]
                continue

            tickers.append(row[0])
            for i in range(1,len(row)):
                if line_count == 0:
                    data_matrix.append([])
                data_matrix[i-1].append(float(row[i]))

            line_count += 1
        return tickers, data_matrix, line_count-1, source_name


def plotData(tickers, data_matrix, plot_caption, figure_title, y_label, percent_matrix=[]):
    x = np.arange(1,len(data_matrix[0])+1,1)
    num_plots = len(data_matrix)
    f, axarr = plt.subplots(num_plots, sharex=True, sharey=True)
    f.text(0.04, 0.5, y_label, va='center', rotation='vertical')
    if percent_matrix != []:
        f.text(0.96, 0.5, 'percentage', va='center', rotation='vertical')
    f.suptitle(figure_title)
    ax2 = []

    for i in range(num_plots):
        l1 = axarr[i].bar(x, data_matrix[i], width=0.75, log=True, alpha=0.5)

    for i in range(num_plots):
        axarr[i].set_xticks(x)
        axarr[i].set_xticklabels(tickers)
        # axarr[i].set_yscale('log')
        axarr[i].yaxis.set_tick_params(labelsize=8)
        axarr[i].xaxis.set_tick_params(rotation=45, labelsize=8)
        # source caption
        axarr[i].text(0.95, 0.9, plot_caption[i],
                        verticalalignment='top', horizontalalignment='right',
                        transform=axarr[i].transAxes,
                        color='black', fontsize=10)

        # plot percent matirx
        if percent_matrix != []:
            print(percent_matrix[i])
            ax2.append(axarr[i].twinx())
            s2 = percent_matrix[i]
            l2, = ax2[i].plot(x, s2, 'rh', alpha=0.6, markersize=4)
            # ax2[i].tick_params('y', colors='r')
            ax2[i].set_ylim(0, 100)

        if i == 0:
            axarr[i].xaxis.set_tick_params(labeltop='on')

    # plt.ylim((10 ** -1, 10 ** 3))
    f.legend((l1, l2), ('Concentration', 'Percentage'), 'upper right')
    plt.show()


def spotSelect(site):
    if site not in ['SP', 'EO', 'LA']:
        print("Invalid site name!")
        exit()

    con_file_name = DATA_FILE_PATH + site + '.csv'
    pct_file_name = DATA_FILE_PATH + site + '_pct.csv'
    y_label = 'Concentration $(ng/m^3)$'

    if site == 'EO':
        figure_title = 'East Oakland'
    elif site == 'SP':
        figure_title = 'San Pablo'
    else:
        figure_title = 'Los Angeles'

    return con_file_name, pct_file_name, figure_title, y_label


if __name__ == '__main__':
    # input site : one of the three ['SP', 'EO', 'LA']
    con_file_name, pct_file_name, figure_title, y_label = spotSelect('SP')

    tickers, data_matrix, line_count, source_name = load_data(con_file_name)
    _, percent_matrix, _, _ = load_data(pct_file_name)

    for row in data_matrix:
        print(row)
    # matrix data pre-processing
    tol = 0.0001
    for i in range(len(data_matrix)):
        for j in range(len(data_matrix[i])):
            if (abs(data_matrix[i][j]) < tol):
                data_matrix[i][j] = tol

    plotData(tickers, data_matrix, source_name, figure_title, y_label, percent_matrix)