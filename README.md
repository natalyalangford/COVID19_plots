# COVID19_plots
Visualization utilities for the COVID-19 data from Johns Hopkins University and US data from the USA Facts website.

This project was developed in and for the Linux environment using Python 3.7.  It does have dependencies
on other modules which can be met by installing those defined the the provided requirements file:
```
sudo -H pip install -r requirements.txt
```
We have used this utility and the bash file included in the repository to generate the following report:
* [Daily Report of Key Plots](https://github.com/natalyalangford/COVID19_plots/blob/master/daily_report/REPORT.md)

## covid19-vi
The *covid19-vi* utility is the main interface for the projects access to the public COVID-19
time series data.  The *--download* option is used to retrieve the latest data from the
sources defined in the project. The data is read with a url request and loaded into a
dataframe.  The dataframe is processed with error checkers, aggretators, and analytics
utilities and then pickled for quicker use by the utility.

Various reports can be generated from the pickled data set by using command line arguments:
```
usage: covid19-vi [-h] [--about] [--minimum MINIMUM] [--columns COLUMNS]
                  [--length LENGTH] [--threshold THRESHOLD]
                  [--mwindow MWINDOW] [--rwindow RWINDOW] [--country COUNTRY]
                  [--state STATE] [--region REGION] [--type TYPE]
                  [--exclude EXCLUDE] [--response RESPONSE] [--sources]
                  [--download] [--saveplot] [--showplot] [--savetable]
                  [--showtable] [--savedir SAVEDIR] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --about               display information about this utility
  --minimum MINIMUM     where applicable, excludes regions where times series shorter than minimum
  --columns COLUMNS     number of columns in table report
  --length LENGTH       data length for sorted reports
  --threshold THRESHOLD threshold of case number to be included
  --mwindow MWINDOW     size of the window for moving avg
  --rwindow RWINDOW     size of the window for rolling days to double
  --country COUNTRY     name of country for state/province reports
  --state STATE         name of state for county reports
  --region REGION       scope of report: country, state, province, county, county-state
  --type TYPE           type of report: confirmed, deaths
  --exclude EXCLUDE     comma separated list of regions to exclude
  --response RESPONSE   response: log, linear, new-total, trajectory, rdtd
  --sources             list sources used by this utility
  --download            download data from sources and save to local pickle
  --saveplot            save plot to a file
  --showplot            display plot
  --savetable           save table to a file
  --showtable           display table
  --savedir SAVEDIR     destination for saving files
  --debug               debug output
```
As an example, the command line arguments to only download and pre-process time series data, execute
the following:
```shell script
covid19-vi --download
```
To display a plot of the confirmed cases for top 20 countries, execute:
```shell script
covid19-vi --type confirmed --region country --length 20 --showplot
```
To display a table of the deaths for top 20 provinces of Canada, execute:
```shell script
covid19-vi --type deaths --region province --country Canada --length 20 --showtable
```
To display a plot of the confirmed cases for top 20 counties of New York, execute:
```shell script
covid19-vi --type confirmed --region county --country US --state NY --length 20 --showplot
```
To display confirmed case rolling days to double trends for countries with more than 200 cases
using a rolling window size of 5 and displaying only trends longer than 10, execute:
```shell script
covid19-vi --type confirmed --region country --threshold 200 --response rdtd --rwindow 5 --minimum 10 --showplot
```

## daily.sh
This bash script is used to generate the plots and tables found in the posted
[daily report](https://github.com/natalyalangford/COVID19_plots/blob/master/daily_report/REPORT.md).

## Reference Material
* Global COVID-19 Data Source:
[CSSEGISandData](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data)
* US COVID-19 Data Source:
[USA Facts](https://usafacts.org/issues/coronavirus/)

## Known Issues
* USA Facts data is a day behind global data from JHU, could be that JHU is using UTC, but state reports 
seem to be lagging what others are reporting.
* Data aggregation function is kludgy and should be rewritten using pivot.

## History
*  1-Apr-20: Implemented rolling days to double plots and metrics
* 31-Mar-20: Implemented trajectory plots and fixed smoothing of new vs total plots
* 29-Mar-20: Implemented new vs total plots
* 26-Mar-20: Corrected error in downloading from USA Facts (removed urllib3)
* 25-Mar-20: Started publishing
[daily report](https://github.com/natalyalangford/COVID19_plots/blob/master/daily_report/REPORT.md).
* 22-Mar-20: Project Initiated
