CPF wind direction & factor contribution
- data_load.py
    + read 2015 & 2016 wd data
    + open file, read row by row, filter out the target site
        * For 2016, check 4th entry of every row
        * For 2015, filter out site ID (buchanan, 5292), (oakland int, 2710), (usc campus, 5297). Then parse
    + save to csv
- wind_main.py
    + read csv
    + pick all dates from factor data, extend 1 to 3 days, count wind
    + pick top dates from factor data, extend, count wind
    + compute ratio, plot