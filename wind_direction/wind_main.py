# combine factor contribution and wind direction
import csv
import collections
import datetime
import matplotlib.pyplot as plt
from math import ceil
import numpy as np

from repo_config import *


def wd_count(wind_data, theta, dates=[], wind_screen = 1.5):
    # theta of one direction
    theta = theta
    direct_count = [0]* int(360/theta)

    if len(dates) == 0:
        # count all dates in wind_data
        for day, wind_list in wind_data.items():
            for wd, ws in wind_list:
                if wd == 'nan':
                    wd = -200
                wd = int(float(wd))
                ws = float(ws)
                if wd<=0 or wd >360 or ws < wind_screen:
                    continue

                direct_count[int((wd+theta/2)/theta)%16] += 1
    else:
        # count only the date in dates
        for d in dates:
            for wd, ws in wind_data[d]:
                if wd == 'nan':
                    wd = -200
                wd = int(float(wd))
                ws = float(ws)
                if wd<=0 or wd >360 or ws < wind_screen:
                    continue

                direct_count[int((wd+theta/2)/theta)%16] += 1

    return direct_count


def read_wd_data(wd_data_file):
    # data container
    # wind_data["date"] = a list of 24 wind directions
    wind_data = collections.defaultdict(list)

    curr_date = ""
    with open(wd_data_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] != curr_date:
                curr_date = row[0]
            wind_data[curr_date].append((row[2], row[3]))

    return wind_data


def read_factor_data(factor_data_file):
    # data container
    factor_data = collections.defaultdict(list)
    factor_names = []
    with open(factor_data_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line = 0
        for row in csv_reader:
            if line == 0:
                # special case
                factor_names = row[1::]
                line += 1
                continue
            factor_data[row[0]] = row[1::]

    return factor_data, factor_names


def get_top_days(factor_data, factor=0, top_ratio=0.5):
    data_pair = collections.defaultdict(float)
    for k, v in factor_data.items():
        data_pair[k] = float(v[factor])

    pick_num = int(len(data_pair) * top_ratio)
    count = 0
    top_dates = []
    for k, v in sorted(data_pair.items(), key=lambda x: x[1], reverse=True):
        top_dates.append(k)
        count += 1
        if count >= pick_num:
            break

    return top_dates


def get_next_day(date):
    # string to date obj
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
    next = date_obj + datetime.timedelta(days=1)
    next_str = datetime.datetime.strftime(next, "%Y-%m-%d")
    return next_str


if __name__ == '__main__':

    # setting
    top_ratio = 0.2
    wd_data_file = ''
    factor_data_file = ''
    site_name = ''
    option = 4
    theta = 22.5
    wind_screen = 2

    # read csv file
    # use wdws, which includes both wind speed and wind direction
    if option == 1: #used this for final results
        wd_data_file = 'oakland_int_wdws_scalar.csv'
        wind_site = 'oakland airport'
        factor_data_file = 'EO.csv'
        site_name = 'EO'
    elif option == 2:
        wd_data_file = 'burbank_airport_wdws_scalar.csv'
        wind_site = 'burbank airport'
        factor_data_file = 'LA.csv'
        site_name = 'LA'
    elif option == 3:
        wd_data_file = 'LA_airport_wdws_scalar.csv'
        factor_data_file = 'LA.csv'
        wind_site = 'LA airport'
        site_name = 'LA'
    elif option == 4:
        wd_data_file = 'buchanan_wdws_scalar.csv'
        factor_data_file = 'SP.csv'
        wind_site = 'buchanan'
        site_name = 'SP'
    elif option == 5:
        wd_data_file = 'buchanan_wd_scalar.csv'
        factor_data_file = 'SP2.csv'
        site_name = 'SP'
    elif option == 6:
        wd_data_file = 'santa_airport_wdws_scalar.csv'  # not good
        factor_data_file = 'LA.csv'
        wind_site = 'santa monica airport'
        site_name = 'LA'
    elif option == 7:
        wd_data_file = 'hawthorne_airport_wdws_scalar.csv'
        factor_data_file = 'LA.csv'
        wind_site = 'Hawthorne Municipal Airport'
        site_name = 'LA'
    else:
        wd_data_file = 'LA-north main street_wd_scalar.csv'
        factor_data_file = 'LA.csv'
        site_name = 'LA-north main street'

    wd_data_file = DATA_FILE_PATH + wd_data_file
    factor_data_file = DATA_FILE_PATH + factor_data_file


    print('wd_data_file: {}'.format(wd_data_file))
    print('site_name: {}'.format(site_name))

    wind_data = read_wd_data(wd_data_file)
    factor_data, factor_names = read_factor_data(factor_data_file)
    num_factors = len(factor_names)

    # pick dates and extend [1 day -> 3 days]
    pick_dates = []
    for day, f_list in factor_data.items():
        pick_dates.append(day)
        # add day+1, day+2
        next = get_next_day(day)
        pick_dates.append(next)
        next_next = get_next_day(next)
        pick_dates.append(next_next)


    # count directions
    all_count = wd_count(wind_data, theta, pick_dates, wind_screen = wind_screen)
    for i in range(len(all_count)):
        if all_count[i] == 0:
            all_count[i] = 1

    # count top and compute ratio
    ratio = [0] * num_factors
    for f in range(0, num_factors):
        top_dates = get_top_days(factor_data, f, top_ratio=top_ratio)
        # extend top dates [1 day -> 3 days]
        top_dates_ext = []
        for day in top_dates:
            top_dates_ext.append(day)
            # add day+1, day+2
            next = get_next_day(day)
            top_dates_ext.append(next)
            next_next = get_next_day(next)
            top_dates_ext.append(next_next)

        # count only for top dates
        select_count = wd_count(wind_data, theta, top_dates_ext, wind_screen)
        print(f, select_count)

        # ratio plot
        ratio[f] = [x/y for x, y in zip(select_count, all_count)]

    # plot polar graph
    thetas = [x*theta/180 * 3.1415 for x in range(int(360/theta))]
    width = [(theta-0.5) / 180 * 3.1415]

    fig, axes = plt.subplots(2, ceil(num_factors/2), subplot_kw=dict(polar=True))


    print(ceil(num_factors/2))
    for f in range(0, num_factors):
        row_fig_num = ceil(num_factors/2)
        x = int(f/row_fig_num)
        y = int(f%row_fig_num)
        axes[x, y].set_theta_zero_location("N")
        axes[x, y].set_theta_direction(-1)
        axes[x, y].bar(thetas, ratio[f],
                                width=width, bottom=0.0, color='r', alpha=0.5)

        # axes[x, y].plot(thetas+[thetas[0]], ratio[f]+[ratio[f][0]], 'ro-', linewidth=3)
        axes[x, y].set_rmax(0.6)
        axes[x, y].set_rticks([x*0.2 for x in range(1,4)])  # less radial ticks
        axes[x, y].set_rlabel_position(60)  # get radial labels away from plotted line

        axes[x, y].grid(True)
        y_position = 1.08
        if x == 1:
            y_position = -0.2

        axes[x, y].set_title("{}".format(factor_names[f]), y=y_position,fontsize=18)

    plt.suptitle('CPF for {}, top {}, with wind speed screening, wind site "{}"'.format(site_name, top_ratio, wind_site), fontsize=20)
    plt.show()
