#!/bin/sh
###########################################################################
## Script to generate plots for daily report
###########################################################################
#
#    Copyright (C) 2019  Ricks-Lab, Natalya Langford
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###########################################################################
set -x
# Download Data
./covid19-vi --download
# Global Reports
./covid19-vi --type confirmed --region country --length 70 --threshold 300 --response trajectory --mwindow 2 --rwindow 5 --minimum 10 --exclude China --saveplot --savedir daily_report
./covid19-vi --type confirmed --region country --length 30 --threshold 300 --response new-total --saveplot --savedir daily_report
./covid19-vi --type confirmed --region country --length 50 --threshold 600 --response rdtd --rwindow 5 --mwindow 3 --minimum 10 --exclude China,Korea --saveplot --savedir daily_report
./covid19-vi --type confirmed --region country --length 20 --columns 12 --saveplot --savetable --savedir daily_report
./covid19-vi --type deaths --region country --length 70 --threshold 30 --response trajectory --mwindow 2 --rwindow 5 --minimum 10 --exclude China --saveplot --savedir daily_report
./covid19-vi --type deaths --region country --length 30 --threshold 30 --response new-total --saveplot --savedir daily_report
./covid19-vi --type deaths --region country --length 50 --threshold 60 --response rdtd --rwindow 5 --minimum 10 --exclude China --saveplot --savedir daily_report
./covid19-vi --type deaths --region country --length 20 --columns 12 --saveplot --savetable --savedir daily_report

# US Reports by State
./covid19-vi --type confirmed --region state --length 80 --threshold 200 --response trajectory --mwindow 2 --rwindow 5 --minimum 6 --saveplot --savedir daily_report
./covid19-vi --type confirmed --region state --country US --length 40 --threshold 100 --response new-total --saveplot --savedir daily_report
./covid19-vi --type confirmed --region state --length 40 --threshold 400 --response rdtd --rwindow 5 --mwindow 3 --minimum 6 --saveplot --savedir daily_report
./covid19-vi --type confirmed --region state --country US --length 20 --columns 12 --saveplot --savetable --savedir daily_report
./covid19-vi --type deaths --region state --country US --length 20 --columns 12 --saveplot --savetable --savedir daily_report

# US Reports by County
./covid19-vi --type confirmed --region county-state --length 50 --threshold 200 --response trajectory --mwindow 2 --rwindow 5 --minimum 8 --saveplot --savedir daily_report
./covid19-vi --type confirmed --region county-state --country US --length 30 --threshold 100 --response new-total --saveplot --savedir daily_report
./covid19-vi --type confirmed --region county-state --length 40 --threshold 300 --response rdtd --rwindow 5 --mwindow 3 --minimum 6 --saveplot --savedir daily_report
./covid19-vi --type confirmed --region county-state --country US --length 20 --columns 11 --saveplot --savetable --savedir daily_report
./covid19-vi --type deaths --region county-state --country US --length 20 --columns 11 --saveplot --savetable --savedir daily_report

# US State State Reports by County
./covid19-vi --type confirmed --region county --country US --state NY --length 20 --columns 12 --threshold 10 --response new-total --saveplot --savetable --savedir daily_report
./covid19-vi --type confirmed --region county --country US --state OR --length 20 --columns 12 --threshold 10 --response new-total --saveplot --savetable --savedir daily_report
./covid19-vi --type confirmed --region county --country US --state CA --length 20 --columns 12 --threshold 10 --response new-total --saveplot --savetable --savedir daily_report
./covid19-vi --type confirmed --region county --country US --state FL --length 20 --columns 12 --threshold 10 --response new-total --saveplot --savetable --savedir daily_report
./covid19-vi --type confirmed --region county --country US --state TX --length 20 --columns 12 --threshold 10 --response new-total --saveplot --savetable --savedir daily_report
