import csv
import re
from repo_config import *


def find_site(row, site_name):
    if len(row) < 4:
        return False
    elif row[3].startswith(site_name):
        return True

    return False


if __name__ == '__main__':

    # parameter
    output_wd = ''
    site = ''
    site_id = ''
    option = 6

    if option == 1:
        output_wd = 'oakland_int_wdws_scalar.csv'
        site = 'Oakland International Airport'
        site_id = '2710'
    elif option == 2:
        output_wd = 'burbank_airport_wdws_scalar.csv'
        site = 'Burbank-Glendale-Pasadena'
        site_id = '2582'
    elif option == 3:
        output_wd = 'LA_airport_wdws_scalar.csv'
        site = 'Los Angeles-International Airport'
        site_id = '2017'
    elif  option == 4:
        output_wd = 'buchanan_wdws_scalar.csv'
        site = 'Buchanan'
        site_id = '5292'
    elif option == 5:
        output_wd = 'santa_airport_wdws_scalar.csv'
        site = 'Santa Monica Municipal Airport'
        site_id = '2059'
    elif option == 6:
        output_wd = 'hawthorne_airport_wdws_scalar.csv'
        site = 'Hawthorne Municipal Airport'
        site_id = '5307'
    else:
        output_wd = 'LA-north main street_wd_scalar.csv'
        site = 'Los Angeles-North Main Street'
        site_id = '2899'

    output_wd = DATA_FILE_PATH + output_wd

    # open wd 2016 file
    # file_wd_2016 = r'C:\Users\weixu\Google Drive\CodingProjects\UFP-master\wind_direction\CA_wd_scalar_2016.csv'
    file_wd_2016 = 'D:\Data\CA_wd_scalar_2016.csv'
    file_ws_2016 = 'D:\Data\CA_ws_scalar_2016.csv'
    wd_2016 = []
    ws_2016 = []

    print('output_wd: {}'.format(output_wd))
    print('site: {}'.format(site))


    print('Processing wd file 2016: {}...'.format(file_wd_2016))
    with open(file_wd_2016) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if find_site(row, site):
                    wd_2016.append([row[7], row[8], row[10]])
                line_count += 1

        print(f'Processed {line_count} lines.')
        print(f'Filter out {len(wd_2016)} lines.')

    print('Processing ws file 2016: {}...'.format(file_ws_2016))
    with open(file_ws_2016) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if find_site(row, site):
                    ws_2016.append([row[7], row[8], row[10]])
                line_count += 1

        print(f'Processed {line_count} lines.')
        print(f'Filter out {len(ws_2016)} lines.')

    wdws_2016 = []
    j = 0
    for i in range(len(wd_2016)):
        while(wd_2016[i][0] != ws_2016[j][0] or wd_2016[i][1] != ws_2016[j][1]):
            print(i, wd_2016[i], '\n', ws_2016[i])
            j += 1
        wdws_2016.append(wd_2016[i]+[ws_2016[j][2]])
        j+= 1
        
    # open wd 2015 file 
    # file_name = r'C:\Users\weixu\Google Drive\CodingProjects\UFP-master\wind_direction\kg_2015.txt'
    file_name = 'D:\Data\kg_2015.txt'
    wdws_2015 = []
    print('Processing wd file 2015: {}...'.format(file_name))
    f = open(file_name, 'r')
    for text in f:
        # find buchanan
        if text.startswith(' '+site_id): #the wind file has one string per row, site_id is the first
            text = re.sub(' ', '', text)
            row = text.split('|')
            date = '{}-{}-{}'.format(row[7], row[8], row[9])
            hour = row[10]
            wd = row[17]
            ws = row[16]
            wdws_2015.append([date, hour, wd, ws])

    # combine and save
    print('Saving to {}...'.format(output_wd))
    filtered = wdws_2015 + wdws_2016
    with open(output_wd, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(filtered)