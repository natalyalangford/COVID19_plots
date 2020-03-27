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
The *covid19-vi* utility is the main interface for the projects access to the public COVID-19 time series
data.  The *--download* option is used to retrieve the latest data from the sources defined in the project.
The data is read with a url request and loaded into a dataframe.  The dataframe is processed with error checkers,
aggretators, and analytics utilities and then pickled for quicker use by the utility.

Various reports can be generated from the pickled data set by using command line arguments:
```
usage: covid19-vi [-h] [--about] [--length LENGTH] [--country COUNTRY]
                  [--state STATE] [--region REGION] [--type TYPE] [--sources]
                  [--download] [--saveplot] [--showplot] [--savetable]
                  [--showtable] [--savedir SAVEDIR] [-d]

optional arguments:
  -h, --help         show this help message and exit
  --about            README
  --length LENGTH    data length for sorted reports
  --country COUNTRY  name of country for state/province report
  --state STATE      name of state for county report
  --region REGION    scope of report: country, state, province, county, county-state
  --type TYPE        type of report: confirmed, deaths
  --sources          list sources used by this utility
  --download         download data from sources and save local pickle
  --saveplot         save plot output to a file
  --showplot         plot output
  --savetable        write table to file
  --showtable        display table
  --savedir SAVEDIR  destination for saving output
  --debug            debug output
```

## daily.sh
This bash script is used to generate the plots and tables found in the posted
[daily report](https://github.com/natalyalangford/COVID19_plots/blob/master/daily_report/REPORT.md).

## Reference Material
* Global COVID-19 Data Source: [CSSEGISandData](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data)
* US COVID-19 Data Source: [USA Facts](https://usafacts.org/issues/coronavirus/)

## Known Issues
* USA Facts data is a day behind global data from JHU, could be that JHU is using UTC, but state reports 
seem to be lagging what others are reporting.
* Data aggregation function is kludgy and should be rewritten using pivot.

## History
* 22-Mar-20: Project Initiated
