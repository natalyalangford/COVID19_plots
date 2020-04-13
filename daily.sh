#!/bin/bash
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
# Set key report parameters
RWIN=5
MWIN=3
TCOLS=12
SDIR="daily_report"
if [[ ! -d  $SDIR ]]
then
    echo "${SDIR} does not exist, exiting..."
    exit
fi
echo "Using directory: ${SDIR}, rwindow: ${RWIN}, mwindow: ${MWIN}, table columns: ${TCOLS}"
# Download Data
./covid19-vi --download --mwindow $MWIN --rwindow $RWIN

set -x
# Global Reports
./covid19-vi --type confirmed --region country --length 70 --threshold 300 --response trajectory --mwindow $MWIN --rwindow $RWIN --minimum 10 --exclude China --saveplot --savedir $SDIR
./covid19-vi --type confirmed --region country --length 30 --threshold 300 --response new-total --saveplot --savedir $SDIR
./covid19-vi --type confirmed --region country --length 50 --threshold 600 --response rdtd --rwindow $RWIN --mwindow $MWIN --minimum 10 --exclude China,Korea --saveplot --savedir $SDIR
./covid19-vi --type confirmed --region country --length 20 --columns $TCOLS --saveplot --savetable --savedir $SDIR
./covid19-vi --type deaths --region country --length 70 --threshold 30 --response trajectory --mwindow $MWIN --rwindow $RWIN --minimum 10 --exclude China --saveplot --savedir $SDIR
./covid19-vi --type deaths --region country --length 30 --threshold 30 --response new-total --saveplot --savedir $SDIR
./covid19-vi --type deaths --region country --length 50 --threshold 60 --response rdtd --rwindow $RWIN --minimum 10 --exclude China --saveplot --savedir $SDIR
./covid19-vi --type deaths --region country --length 20 --columns $TCOLS --saveplot --savetable --savedir $SDIR

# US Reports by State
./covid19-vi --type confirmed --region state --length 80 --threshold 300 --response trajectory --mwindow $MWIN --rwindow $RWIN --minimum 6 --saveplot --savedir $SDIR
./covid19-vi --type confirmed --region state --country US --length 40 --threshold 100 --response new-total --saveplot --savedir $SDIR
./covid19-vi --type confirmed --region state --length 40 --threshold 400 --response rdtd --rwindow $RWIN --mwindow $MWIN --minimum 6 --saveplot --savedir $SDIR
./covid19-vi --type confirmed --region state --country US --length 20 --columns $TCOLS --saveplot --savetable --savedir $SDIR
./covid19-vi --type deaths --region state --country US --length 20 --columns $TCOLS --saveplot --savetable --savedir $SDIR

# US Reports by County
./covid19-vi --type confirmed --region county-state --length 50 --threshold 300 --response trajectory --mwindow $MWIN --rwindow $RWIN --minimum 8 --saveplot --savedir $SDIR
./covid19-vi --type confirmed --region county-state --country US --length 30 --threshold 100 --response new-total --saveplot --savedir $SDIR
./covid19-vi --type confirmed --region county-state --length 40 --threshold 300 --response rdtd --rwindow $RWIN --mwindow $MWIN --minimum 6 --saveplot --savedir $SDIR
./covid19-vi --type confirmed --region county-state --country US --length 20 --columns $TCOLS --saveplot --savetable --savedir $SDIR
./covid19-vi --type deaths --region county-state --country US --length 20 --columns $TCOLS --saveplot --savetable --savedir $SDIR

# US State State Reports by County
./covid19-vi --type confirmed --region county --country US --state NY --length 20 --columns $TCOLS --threshold 10 --response new-total --saveplot --savetable --savedir $SDIR
./covid19-vi --type confirmed --region county --country US --state OR --length 20 --columns $TCOLS --threshold 10 --response new-total --saveplot --savetable --savedir $SDIR
./covid19-vi --type confirmed --region county --country US --state CA --length 20 --columns $TCOLS --threshold 10 --response new-total --saveplot --savetable --savedir $SDIR
./covid19-vi --type confirmed --region county --country US --state FL --length 20 --columns $TCOLS --threshold 10 --response new-total --saveplot --savetable --savedir $SDIR
./covid19-vi --type confirmed --region county --country US --state TX --length 20 --columns $TCOLS --threshold 10 --response new-total --saveplot --savetable --savedir $SDIR
