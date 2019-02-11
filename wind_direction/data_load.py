import csv
import re


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
    option = 5

    if option == 1:
        output_wd = 'oakland_int_wd_scalar.csv'
        site = 'Oakland International Airport'
        site_id = '2710'
    elif option == 2:
        output_wd = 'usc_campus_wd_scalar.csv'
        site = 'Los Angeles - USC Campus Downtown'
        site_id = '5297'
    elif option == 3:
        output_wd = 'LA_airport_wd_scalar.csv'
        site = 'Los Angeles-International Airport'
        site_id = '2017'
    elif  option == 4:
        output_wd = 'buchanan_wd_scalar.csv'
        site = 'Buchanan'
        site_id = '5292'
    else:
        output_wd = 'LA-north main street_wd_scalar.csv'
        site = 'Los Angeles-North Main Street'
        site_id = '2899'
    # open wd 2016 file
    file_wd_2016 = r'C:\Users\weixu\Google Drive\CodingProjects\UFP-master\wind_direction\CA_wd_scalar_2016.csv'
    filtered_2016 = []

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
                    filtered_2016.append([row[7], row[8], row[10]])
                line_count += 1

        print(f'Processed {line_count} lines.')
        print(f'Filter out {len(filtered_2016)} lines.')
        
        
    # open wd 2015 file 
    file_name = r'C:\Users\weixu\Google Drive\CodingProjects\UFP-master\wind_direction\kg_2015.txt'
    filtered_2015 = []
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
            filtered_2015.append([date, hour, wd])

    # combine and save
    print('Saving to {}...'.format(output_wd))
    filtered = filtered_2015 + filtered_2016
    with open(output_wd, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(filtered)