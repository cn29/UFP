import matplotlib.pyplot as plt
import numpy as np
import csv

from repo_config import *


def readCSV(file_name, plot_num):
    print(1)
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = 29*2
        line_count = 0
        tickers = []
        data_matrix = np.zeros([plot_num, row_count], dtype=float)
        for row in csv_reader:
            tickers.append(row[0])
            for i in range(1, plot_num+1):
                data_matrix[i-1][line_count] = float(row[i])
            line_count += 1
        return tickers, data_matrix, line_count


def plotData(tickers, data_matrix, plot_name, figure_title, y_label):
    x = np.arange(1,len(data_matrix[0])+1,1)
    num_plots = len(data_matrix)
    f, axarr = plt.subplots(num_plots, sharex=True, sharey=True)
    f.text(0.04, 0.5, y_label, va='center', rotation='vertical')
    f.suptitle(figure_title)
    for i in range(num_plots):
        axarr[i].bar(x, data_matrix[i], width=0.75, log=True)

    for i in range(num_plots):
        axarr[i].set_xticks(x)
        axarr[i].set_xticklabels(tickers)
        # axarr[i].set_yscale('log')
        axarr[i].yaxis.set_tick_params(labelsize=8)
        axarr[i].xaxis.set_tick_params(rotation=45, labelsize=8)

        if i == 0:
            axarr[i].xaxis.set_tick_params(labeltop='on')

    # add plot name
    for i in range(num_plots):
        f.text(0.86, 0.19+i*0.132, plot_name[i], ha='right', va='center')

    plt.ylim((10 ** -3, 10 ** 2))
    plt.show()


def spotSelect(spot):
    if spot == 'EO':
        file_name = 'EO.csv'
        plot_name = ['Wood burning', 'Traffic/meat cooking', 'EC3', 'Shipping', 'Sea salt/dust', 'Sn', 'Sb']
        figure_title = 'East Oakland'
        y_label = 'Concentration $(\mu g/m^3)$'
        plot_num = 7
    elif spot == 'SP':
        file_name = 'SP.csv'
        plot_name = ['Wood burning/meat cooking', 'Traffic', 'Shipping', 'Sea salt/dust', 'Sn', 'Sb']
        figure_title = 'San Pablo'
        y_label = 'Concentration $(\mu g/m^3)$'
        plot_num = 6
    else:
        file_name = 'LA.csv'
        plot_name = ['Wood burning/meat cooking', 'Traffic', 'Shipping', 'Sea salt/dust', 'Sn', 'Sb']
        figure_title = 'Los Angeles'
        y_label = 'Concentration $(\mu g/m^3)$'
        plot_num = 6

    file_name = DATA_FILE_PATH + file_name
    return file_name, plot_name, figure_title, y_label, plot_num


if __name__ == '__main__':
    file_name, plot_name, figure_title, y_label, plot_num = spotSelect('LA')

    tickers, data_matrix, line_count = readCSV(file_name, plot_num)
    data_matrix_cut = data_matrix[:,:line_count]

    # matrix data pre-processing
    tol = 0.0001
    for i in range(len(data_matrix_cut)):
        for j in range(len(data_matrix_cut[i])):
            if (abs(data_matrix_cut[i][j]) < tol):
                data_matrix_cut[i][j] = tol


    plotData(tickers, data_matrix_cut, plot_name[::-1], figure_title, y_label)