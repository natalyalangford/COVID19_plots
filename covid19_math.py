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


class CovidMath:
    """
    Class for time series analytics.
    """

    @classmethod
    def series_rolling_doubling_time(cls, t_list, lookback):
        """
        Returns truncated list with max length and max values
        :param t_list: List of numbers
        :type t_list: list
        :param lookback: Size of the window
        :type lookback: int
        :return: Rolling double time as a list
        :rtype: list
        >>> CovidMath.series_rolling_doubling_time([200, 239, 267, 314, 314, 559, 689, 886, 1058, 1243, 1486, 1795, 2257, 2815, 3401, 3743, 4269, 4937, 6235, 7284, 9134, 10836, 11899], 5)
        [nan, 7.78, 7.2, 6.15, 7.68, 4.08, 3.66, 3.34, 2.85, 4.34, 4.51, 4.91, 4.57, 4.24, 4.19, 4.72, 5.44, 6.17, 5.72, 5.21, 4.56, 4.41, 5.36]
        >>> CovidMath.series_rolling_doubling_time([200.0, 239.0, 267.0, 314.0, 314.0, 559.0, 689.0, 886.0, 1058.0, 1243.0], 5)
        [nan, 7.78, 7.2, 6.15, 7.68, 4.08, 3.66, 3.34, 2.85, 4.34]
        >>> CovidMath.series_rolling_doubling_time([200, 239, 267, 314, 314, 559, 689, 886], 5)
        [nan, 7.78, 7.2, 6.15, 7.68, 4.08, 3.66, 3.34]
        >>> CovidMath.series_rolling_doubling_time([np.nan, 239, 267, 314, 314, 559, 689, 886, 1058, 1243, 1486, 1795, 2257, 2815, 3401, 3743, 4269, 4937, 6235, 7284, 9134, 10836, 11899], 5)
        [nan, nan, 12.51, 7.62, 10.16, 4.08, 3.66, 3.34, 2.85, 4.34, 4.51, 4.91, 4.57, 4.24, 4.19, 4.72, 5.44, 6.17, 5.72, 5.21, 4.56, 4.41, 5.36]
        >>> CovidMath.series_rolling_doubling_time([239, 267], 5)
        [nan, 12.51]
        >>> CovidMath.series_rolling_doubling_time([239], 5)
        [nan]
        >>> CovidMath.series_rolling_doubling_time([], 5)
        [nan]
        """
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
    def series_doubling_time(cls, target_list):
        """
        Returns truncated list with max length and max values
        :param target_list: List of numbers
        :type target_list: list
        :return: Number of days to double
        :rtype: float
        .. note: https://blog.datawrapper.de/weekly-chart-coronavirus-doublingtimes/
        >>> CovidMath.series_doubling_time([6235, 7284, 9134, 10836, 11899])
        5.36
        >>> CovidMath.series_doubling_time([np.nan, 7284, 9134, 10836, 11899])
        5.65
        >>> CovidMath.series_doubling_time([0, 0, 0, 0, 0]) is np.nan
        True
        >>> CovidMath.series_doubling_time([]) is np.nan
        True
        """
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
        return ret_val

    @classmethod
    def truncate_series(cls, target_list, length, value):
        """
        Returns truncated list with max length and max values
        :param target_list: List of numbers
        :type target_list: list
        :param length: max list length
        :type length: int
        :param value: max value in a time series
        :type value: int
        :return: The resultant index or None is never met
        :rtype: list
        >>> CovidMath.truncate_series([1, 2, 3, 4, 5, 6, 7], 4, 6)
        [1, 2, 3, 4]
        >>> CovidMath.truncate_series([1, 2, 3, 4, 5, 6, 7], 6, 3)
        [1, 2, 3]
        >>> CovidMath.truncate_series([1, 2, 3, 4, 5, 6, 7], 99, 99)
        [1, 2, 3, 4, 5, 6, 7]
        >>> CovidMath.truncate_series([], 6, 3)
        []
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
    def threshold_index(cls, t_list, threshold):
        """
        Return the index of the first item >= threshold
        :param t_list: List of numbers
        :type t_list: list
        :param threshold: The threshold
        :type threshold: int
        :return: The resultant index or None if never met
        :rtype: Union(int, None)
        >>> CovidMath.threshold_index([1, 2, 3, 4, 5, 6, 7], 4)
        3
        >>> CovidMath.threshold_index([1, 2, 3, 4, 5, 6, 7], 0)
        0
        >>> CovidMath.threshold_index([1, 2, 3, 4, 5, 6, 7], 10) is None
        True
        >>> CovidMath.threshold_index([], 10) is None
        True
        """
        for i, x in enumerate(t_list):
            if x >= threshold:
                return i
        return None

    @classmethod
    def start_at_threshold(cls, t_list, threshold):
        """
        Return a list that starts at the first item >= threshold
        :param t_list: List of numbers
        :type t_list: list
        :param threshold: The threshold
        :type threshold: int
        :return: The new list
        :rtype: list
        >>> CovidMath.start_at_threshold([1, 2, 3, 4, 5, 6, 7], 4)
        [4, 5, 6, 7]
        >>> CovidMath.start_at_threshold([1, 2, 3, 4, 5, 6, 7], 0)
        [1, 2, 3, 4, 5, 6, 7]
        >>> CovidMath.start_at_threshold([1, 2, 3, 4, 5, 6, 7], 10)
        []
        >>> CovidMath.start_at_threshold([], 10)
        []
        """
        return [y_val for i, y_val in enumerate(t_list) if min(t_list[i:]) >= threshold]

    @classmethod
    def moving_average(cls, list_values, lookback):
        """
        Return a list that is the moving average of the original list with windows size of lookback
        :param list_values: List of numbers
        :type list_values: list
        :param lookback: Size of the window
        :type lookback: int
        :return: The new list
        :rtype: list
        >>> CovidMath.moving_average([0, 654, 287, 493, 684, 809, 2651, 588, 2068, 1693], 2)
        [0, 327.0, 470.5, 390.0, 588.5, 746.5, 1730.0, 1619.5, 1328.0, 1880.5]
        >>> CovidMath.moving_average([0, 654, 287, 493, 684, 809, 2651, 588, 2068, 1693], 3)
        [0, 327.0, 313.67, 478.0, 488.0, 662.0, 1381.33, 1349.33, 1769.0, 1449.67]
        >>> CovidMath.moving_average([2068, 1693], 3)
        [2068, 1880.5]
        >>> CovidMath.moving_average([1693], 3)
        [1693]
        >>> CovidMath.moving_average([], 3)
        []
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
    def total_to_increment(cls, list_orig):
        """
        Return a list that is the difference of subsequent items with the first item set to NAN
        :param list_orig: List of numbers
        :type list_orig: list
        :return: The new list
        :rtype: list
        >>> CovidMath.total_to_increment([0, 654, 941, 1434, 2118, 2927, 5578, 6166, 8234, 9927])
        [nan, 654, 287, 493, 684, 809, 2651, 588, 2068, 1693]
        >>> CovidMath.total_to_increment([0, 654, 941, 1434, 2118, 2000, 5578, 6166, 8234, 9927])
        [nan, 654, 287, 493, 684, -118, 3578, 588, 2068, 1693]
        >>> CovidMath.total_to_increment([654])
        [654]
        >>> CovidMath.total_to_increment([])
        []
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
