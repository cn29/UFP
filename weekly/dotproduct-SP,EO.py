import csv

data=[]
with open ('C:/Users/weixu/Google Drive/Wei/Research/python3/project1/data/dotproduct-SP,EO.csv') as csvfile:
    readcsv = csv.reader(csvfile,delimiter=',')
    for row in readcsv:
        data_row=[]
        for element in row:
            data_row.append(element)

        data.append = (data_row)


    for i in range(1,8)
    for row in data:
