#!/usr/bin/env python3
""" covid19-math  -  Analytics functions in support of covid19_plots

    Copyright (C) 2020  Natalya Langford

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
__author__ = 'Natalya Langford'
__copyright__ = 'Copyright (C) 2020 Natalya Langford'
__credits__ = ['Ricks-Lab - Collaborator']
__license__ = 'GNU General Public License'
__program_name__ = 'covid19-math'
__version__ = 'v1.0.0'
__maintainer__ = 'Natalya Langford'
__status__ = 'Stable Release'
__docformat__ = 'reStructuredText'
# pylint: disable=multiple-statements
# pylint: disable=line-too-long

import math as math
import numpy as np
from typing import List, Union

TimeSeriesList = List[Union[int, float]]


class CovidMath:
    """
    Class for time series analytics.
    """
    @classmethod
    def series_rolling_doubling_time(cls, t_list: TimeSeriesList, lookback: int) -> TimeSeriesList:
        """
        Returns a new time series list which is the rolling dtd calc on the provided list.

        :param t_list: A time series of numbers in a list
        :param lookback: Size of the window
        :return: Rolling double time as a list
        """
        if not isinstance(lookback, (int, float, np.int64)):
            raise TypeError('Window size must be numeric')
        if not all(isinstance(n, (int, float, np.int64)) for n in t_list):
            raise TypeError('Non numeric values in time series not allowed')
        if lookback <= 1:
            raise ValueError('Window size must be >= 1')
        if len(t_list) <= 1: return [np.nan]
        list_new = [np.nan] * len(t_list)
        if lookback > len(t_list): lookback = len(t_list)
        for i in range(lookback - 1, len(t_list)):
            win_e = i + 1
            win_s = i - (lookback - 1)
            list_new[i] = CovidMath.series_doubling_time(t_list[win_s: win_e])
        win_s = 0
        for win_e in range(lookback, 0, -1):
            list_new[win_e-1] = CovidMath.series_doubling_time(t_list[win_s: win_e])
        return list_new

    @classmethod
    def series_doubling_time_mwin(cls, target_list: TimeSeriesList, rwin: int, mwin: int) -> float:
        """
        Calculate days to double for last rwin of the moving avg of the given time series.

        :param target_list:  Target time series data
        :param rwin: Window size for doubling time
        :param mwin: Window size for moving average
        :return: The days to double value
        """
        if not isinstance(rwin, (int, float, np.int64)) or not isinstance(mwin, (int, float, np.int64)):
            raise TypeError('Window size must be numeric')
        if not all(isinstance(n, (int, float, np.int64)) for n in target_list):
            raise TypeError('Non numeric values in time series not allowed')
        if rwin < 1 or mwin < 1:
            raise ValueError('Window size must be >= 1')
        if rwin < 1 or mwin < 1:
            return np.nan
        m_list = cls.moving_average(target_list, mwin)
        return cls.series_doubling_time(m_list[-rwin:])

    @classmethod
    def series_doubling_time(cls, target_list: TimeSeriesList) -> float:
        """
        Returns the overall days to double for the given list.
        
        :param target_list: List of numbers
        :return: Number of days to double

        .. note: https://blog.datawrapper.de/weekly-chart-coronavirus-doublingtimes/
        """
        if not all(isinstance(n, (int, float, np.int64)) for n in target_list):
            raise TypeError('Non numeric values in time series not allowed')
        if len(target_list) <= 1: return np.nan
        if max(target_list) == 0: return np.nan
        t_list = target_list[:]
        win_s = 0
        win_e = len(t_list)
        while (t_list[win_s] == 0 or t_list[win_s] is np.nan) or not isinstance(t_list[win_s], (int, float, np.int64)):
            win_s += 1
        while (t_list[win_e-1] == 0 or t_list[win_e-1] is np.nan) or \
                not isinstance(t_list[win_e-1], (int, float, np.int64)):
            # Maybe this should return 0 instead
            win_e -= 1
        if win_s >= win_e: return np.nan
        t_list = t_list[win_s: win_e]
        try:
            ret_val = round(len(t_list)*math.log(2)/math.log(t_list[-1]/t_list[0]), 2)
        except ArithmeticError:
            ret_val = np.nan
        except ValueError as err:
            # print('Warning: {}\n  {}'.format(err, target_list))
            # Confirmed caused by negative value
            ret_val = np.nan
        return ret_val

    @classmethod
    def truncate_series(cls, target_list: TimeSeriesList, length: int, value: int) -> TimeSeriesList:
        """
        Returns truncated list with max length and max values.
        
        :param target_list: List of numbers
        :param length: max list length
        :param value: max value in a time series
        :return: The resultant index or None is never met
        """
        t_list = target_list[:]
        if len(t_list) > length:
            t_list = t_list[0:length]
        i = len(t_list)
        for i, t_item in enumerate(t_list):
            if t_item >= value:
                break
        return t_list[:i+1]

    @classmethod
    def threshold_index(cls, t_list: TimeSeriesList, threshold: int) -> Union[int, None]:
        """
        Return the index of the first item >= threshold.
        
        :param t_list: List of numbers
        :param threshold: The threshold
        :return: The resultant index or None if never met
        """
        for i, x in enumerate(t_list):
            if x >= threshold:
                return i
        return None

    @classmethod
    def start_at_threshold(cls, t_list: TimeSeriesList, threshold: int) -> TimeSeriesList:
        """
        Return a list that starts at the first item >= threshold.
        
        :param t_list: List of numbers
        :param threshold: The threshold
        :return: The new list
        """
        return [y_val for i, y_val in enumerate(t_list) if min(t_list[i:]) >= threshold]

    @classmethod
    def moving_average(cls, list_values: TimeSeriesList, lookback: int) -> TimeSeriesList:
        """
        Return a list that is the moving average of the original list with windows size of lookback.
        
        :param list_values: List of numbers
        :param lookback: Size of the window
        :return: The new list
        """
        if not list_values: return list_values
        if lookback == 1 or len(list_values) == 1: return list_values
        list_new = list_values[:]
        for i in range(lookback - 1, len(list_values)):
            win_e = i + 1
            win_s = i - (lookback - 1)
            list_new[i] = round(float(np.nansum(list_values[win_s: win_e])) / float(lookback), 2)
        for i in range(1, lookback - 1):
            win_e = i + 1
            list_new[i] = round(float(np.nansum(list_values[0: win_e])) / float(i+1), 2)
        return list_new

    @classmethod
    def total_to_increment(cls, list_orig: TimeSeriesList) -> TimeSeriesList:
        """
        Return a list that is the difference of subsequent items with the first item set to NAN.
        
        :param list_orig: List of numbers
        :return: The new list
        """
        list_new = list_orig[:]
        for i in range(0, len(list_orig)):
            if i == 0:
                list_new[i] = list_orig[i] if list_orig[i] > 0 else np.NaN
            else:
                list_new[i] = (list_orig[i] - list_orig[i - 1])
        return list_new


if __name__ == '__main__':
    import doctest
    doctest.testmod()
