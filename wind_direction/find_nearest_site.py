import csv
import re
from repo_config import *
import numpy as np



if __name__ == '__main__':
    file_wd_2016 = 'D:\Data\CA_wd_scalar_2016.csv'

    target_lati = 0
    target_longi = 0

    # -----
    option = 1
    if option == 1:
        # SP
        target_lati = 37.960
        target_longi = -122.357
    else:
        # LA
        target_lati = 34.022012
        target_longi = -118.284286

    nearest = []
    dist = 10000
    print('Processing wd file 2016: {}...'.format(file_wd_2016))
    with open(file_wd_2016) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if len(row) < 6:
                continue
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                lati = float(row[5])
                longi = float(row[6])
                tmp_dist = np.linalg.norm([target_lati-lati, target_longi-longi])
                if dist > tmp_dist:
                    dist = tmp_dist
                    nearest = row
                line_count += 1

    print(nearest, dist)
