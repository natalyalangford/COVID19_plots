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
./covid19-vi --type confirmed --region country --length 20 --saveplot --savedir daily_report
./covid19-vi --type deaths --region country --length 20 --saveplot --savedir daily_report

./covid19-vi --type confirmed --region state --country US --length 20 --saveplot --savedir daily_report
./covid19-vi --type deaths --region state --country US --length 20 --saveplot --savedir daily_report

./covid19-vi --type confirmed --region county --country US --state NY --length 20 --saveplot --savedir daily_report
./covid19-vi --type confirmed --region county --country US --state OR --length 20 --saveplot --savedir daily_report
./covid19-vi --type confirmed --region county --country US --state CA --length 20 --saveplot --savedir daily_report
./covid19-vi --type confirmed --region county --country US --state FL --length 20 --saveplot --savedir daily_report
./covid19-vi --type confirmed --region county --country US --state TX --length 20 --saveplot --savedir daily_report
