import csv
import re


def find_site(row, site_name='Buchanan'):
    if len(row) < 4:
        return False
    elif row[3].startswith(site_name):
        return True

    return False


if __name__ == '__main__':
    output_wd = 'buchanan_wd_scalar.csv'
    
    # open wd 2016 file
    file_wd_2016 = 'D:\Data\CA_wd_scalar_2016.csv'
    filtered_2016 = []

    print('Processing wd file 2016: {}...'.format(file_wd_2016))
    with open(file_wd_2016) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if find_site(row):
                    filtered_2016.append([row[7], row[8], row[10]])
                line_count += 1

        print(f'Processed {line_count} lines.')
        print(f'Filter out {len(filtered_2016)} lines.')
        
        
    # open wd 2015 file 
    file_name = 'D:\Data\kg_2015.txt'
    filtered_2015 = []
    print('Processing wd file 2015: {}...'.format(file_name))
    f = open(file_name, 'r')
    for text in f:
        # find buchanan
        if text.startswith(' 5292'):
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