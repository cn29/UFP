import csv
import numpy
import pandas
import time
import datetime

if __name__ == '__main__':

    site1 = 'KCALOSAN107'
    site2 = 'KCARICHM10'
    site = site2
    file_name = './data_files/'+site+'.df'
    print('Reading '+file_name)
    crawler_save = pandas.read_pickle(file_name)

    filter_wd = []
    for row in crawler_save.itertuples(index=True, name='Pandas'):
        date = getattr(row, 'Index').to_datetime()
        day = date.strftime("%Y-%m-%d")
        hour = int(date.strftime("%H"))
        wd = getattr(row, 'Wdir')
        ws = getattr(row, 'Wspd')
        if float(ws) < 0.1:
            continue
        filter_wd.append([day, hour, wd])


    # save to csv
    output_wd = './data_files/'+site+'_wd_scalar.csv'
    print('Saving to {}...'.format(output_wd))
    with open(output_wd, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(filter_wd)