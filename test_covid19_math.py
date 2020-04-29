"""Test suite to accompany color_tiles.py"""

import unittest
import numpy as np
import covid19_math as cvm

# pylint: disable=line-too-long
# pylint: disable=bad-continuation


def round_list(l: list, ndigits: int) -> list:
    return [round(e, ndigits=ndigits) for e in l]


class Test_0_series_rolling_doubling_time(unittest.TestCase):
    def setUp(self) -> None:
        print('Test_0')
        self.test_func = cvm.CovidMath.series_rolling_doubling_time
        self.test_func_name = 'series_rolling_doubling_time'
        self.test_equal = {'test1': {'argument': ([200, 239, 267, 314, 314, 559, 689, 886, 1058, 1243, 1486,
                                                  1795, 2257, 2815, 3401, 3743, 4269, 4937, 6235, 7284,
                                                  9134, 10836, 11899], 5),
                                     'response': [np.nan, 7.78, 7.20, 6.15, 7.68, 4.08, 3.66, 3.34, 2.85, 4.34,
                                                  4.51, 4.91, 4.57, 4.24, 4.19, 4.72, 5.44, 6.17, 5.72, 5.21,
                                                  4.56, 4.41, 5.36]},
                           'test2': {'argument': ([200.0, 239.0, 267.0, 314.0, 314.0, 559.0, 689.0, 886.0, 1058.0,
                                                  1243.0], 5),
                                     'response': [np.nan, 7.78, 7.2, 6.15, 7.68, 4.08, 3.66, 3.34, 2.85, 4.34]},
                           'test3': {'argument': ([200, 239, 267, 314, 314, 559, 689, 886], 5),
                                     'response': [np.nan, 7.78, 7.2, 6.15, 7.68, 4.08, 3.66, 3.34]},
                           'test4': {'argument': ([np.nan, 239, 267, 314, 314, 559, 689, 886, 1058, 1243,
                                                   1486, 1795, 2257, 2815, 3401, 3743, 4269, 4937, 6235,
                                                   7284, 9134, 10836, 11899], 5),
                                     'response': [np.nan, np.nan, 12.51, 7.62, 10.16, 4.08, 3.66, 3.34, 2.85,
                                                  4.34, 4.51, 4.91, 4.57, 4.24, 4.19, 4.72, 5.44, 6.17, 5.72,
                                                  5.21, 4.56, 4.41, 5.36]},
                           'test5': {'argument': ([239, 267], 5),
                                     'response': [np.nan, 12.51]},
                           'test6': {'argument': ([239], 5),
                                     'response': [np.nan]},
                           'test7': {'argument': ([], 5),
                                     'response': [np.nan]}}

        self.test_type = {'test1': {'argument': ([200, '239b', 267, 314, 314, 559, 689, '886b'], 5),
                                    'response': TypeError},
                          'test2': {'argument': ([200, 239, 267, 314, 314, 559, 689, 886], 'five'),
                                    'response': TypeError}}

        self.test_value = {'test1': {'argument': ([200, 239, 267, 314, 314, 559, 689, 886], -1),
                                     'response': ValueError}}

    def test_1_equal(self):
        for test_name, test_case in self.test_equal.items():
            print('Running {} test_equal type: {}'.format(self.test_func_name, test_name))
            np.testing.assert_equal(round_list(self.test_func(*test_case['argument']), 2),
                                    round_list(test_case['response'], 2))

    def test_2_type(self):
        for test_name, test_case in self.test_type.items():
            print('Running {} test_type type: {}'.format(self.test_func_name, test_name))
            self.assertRaises(test_case['response'], self.test_func, *test_case['argument'])

    def test_3_value(self):
        for test_name, test_case in self.test_value.items():
            print('Running {} test_value type: {}'.format(self.test_func_name, test_name))
            self.assertRaises(test_case['response'], self.test_func, *test_case['argument'])


class Test_1_series_doubling_time_mwin(unittest.TestCase):
    def setUp(self) -> None:
        print('Test_1')
        self.test_func = cvm.CovidMath.series_doubling_time_mwin
        self.test_func_name = 'series_doubling_time_mwin'
        self.test_equal = {'test1': {'argument': ([200, 239, 267, 314, 314, 559, 689, 886, 1058, 1243, 1486,
                                                  1795, 2257, 2815, 3401, 3743, 4269, 4937, 6235, 7284,
                                                  9134, 10836, 11899], 5, 3),
                                     'response': 4.782915143}}
        self.test_type = {'test1': {'argument': ([200, 239, 267, 314, 314, 559, 689, 886], 'three', 5),
                                    'response': TypeError},
                          'test2': {'argument': ([np.nan, 239, 267, 314, 314, 559, 689, 886, 1058, 1243,
                                                 '1486', 1795, 2257, 2815, 3401, 3743, 4269, 4937, 6235,
                                                  7284, 9134, 10836, 11899], 5, 3),
                                    'response': TypeError}}
        self.test_value = {'test1': {'argument': ([200, 239, 267, 314, 314, 559, 689, 886], 0, 1),
                                     'response': ValueError},
                           'test2': {'argument': ([np.nan, 239, 267, 314, 314, 559, 689, 886, 1058, 1243,
                                                   1486, 1795, 2257, 2815, 3401, 3743, 4269, 4937, 6235,
                                                   7284, 9134, 10836, 11899], 3, -2),
                                     'response': ValueError}}

    def test_1_equal(self):
        for test_name, test_case in self.test_equal.items():
            print('Running {} test_equal type: {}'.format(self.test_func_name, test_name))
            self.assertEqual(round(self.test_func(*test_case['argument']), 7), round(test_case['response'], 7))

    def test_2_type(self):
        for test_name, test_case in self.test_type.items():
            print('Running {} test_type type: {}'.format(self.test_func_name, test_name))
            self.assertRaises(test_case['response'], self.test_func, *test_case['argument'])

    def test_3_value(self):
        for test_name, test_case in self.test_value.items():
            print('Running {} test_value type: {}'.format(self.test_func_name, test_name))
            self.assertRaises(test_case['response'], self.test_func, *test_case['argument'])


class Test_2_series_doubling_time(unittest.TestCase):
    def setUp(self) -> None:
        print('Test_2')
        self.test_func = cvm.CovidMath.series_doubling_time
        self.test_func_name = 'series_doubling_time'
        self.test_equal = {'test1': {'argument': ([6235, 7284, 9134, 10836, 11899]),
                                     'response': 5.36},
                           'test2': {'argument': ([np.nan, 7284, 9134, 10836, 11899]),
                                     'response': 5.65}}
        self.test_is = {'test1': {'argument': ([0, 0, 0, 0, 0]),
                                  'response': np.nan},
                        'test2': {'argument': ([]),
                                  'response': np.nan}}
        self.test_type = {'test1': {'argument': ([6235, '7284', 9134, 10836, 11899]),
                                    'response': TypeError}}

    def test_1_equal(self):
        for test_name, test_case in self.test_equal.items():
            print('Running {} test_equal type: {}'.format(self.test_func_name, test_name))
            self.assertEqual(round(self.test_func(test_case['argument']), 2), round(test_case['response'], 2))

    def test_2_is(self):
        for test_name, test_case in self.test_is.items():
            print('Running {} test_is type: {}'.format(self.test_func_name, test_name))
            self.assertIs(self.test_func(test_case['argument']), test_case['response'])

    def test_3_type(self):
        for test_name, test_case in self.test_type.items():
            print('Running {} test_type type: {}'.format(self.test_func_name, test_name))
            self.assertRaises(test_case['response'], self.test_func, test_case['argument'])


class Test_3_truncate_series(unittest.TestCase):
    def setUp(self) -> None:
        print('Test_3')
        self.test_func = cvm.CovidMath.truncate_series
        self.test_func_name = 'truncate_series'
        self.test_equal = {'test1': {'argument': ([1, 2, 3, 4, 5, 6, 7], 4, 6),
                                     'response': [1, 2, 3, 4]},
                           'test2': {'argument': ([1, 2, 3, 4, 5, 6, 7], 6, 3),
                                     'response': [1, 2, 3]},
                           'test3': {'argument': ([1, 2, 3, 4, 5, 6, 7], 99, 99),
                                     'response': [1, 2, 3, 4, 5, 6, 7]},
                           'test4': {'argument': ([], 6, 3),
                                     'response': []}}
        self.test_type = {'test1': {'argument': ([1, 2, 3, 4, 5, 6, 7], 99, 'ninety-nine'),
                                    'response': TypeError}}

    def test_1_equal(self):
        for test_name, test_case in self.test_equal.items():
            print('Running {} test_equal type: {}'.format(self.test_func_name, test_name))
            self.assertEqual(self.test_func(*test_case['argument']), test_case['response'])

    def test_2_type(self):
        for test_name, test_case in self.test_type.items():
            print('Running {} test_type type: {}'.format(self.test_func_name, test_name))
            self.assertRaises(test_case['response'], self.test_func, *test_case['argument'])


class Test_4_threshold_index(unittest.TestCase):
    def setUp(self) -> None:
        print('Test_4')
        self.test_func = cvm.CovidMath.threshold_index
        self.test_func_name = 'threshold_index'
        self.test_equal = {'test1': {'argument': ([1, 2, 3, 4, 5, 6, 7], 4),
                                     'response': 3},
                           'test2': {'argument': ([1, 2, 3, 4, 5, 6, 7], 0),
                                     'response': 0}}
        self.test_is = {'test1': {'argument': ([1, 2, 3, 4, 5, 6, 7], 10),
                                  'response': None},
                        'test2': {'argument': ([], 10),
                                  'response': None}}
        self.test_type = {'test1': {'argument': (['1', 2, 3, 4, 5, 6, 7], 10),
                                    'response': TypeError}}

    def test_1_equal(self):
        for test_name, test_case in self.test_equal.items():
            print('Running {} test_equal type: {}'.format(self.test_func_name, test_name))
            self.assertEqual(self.test_func(*test_case['argument']), test_case['response'])

    def test_2_is(self):
        for test_name, test_case in self.test_is.items():
            print('Running {} test_is type: {}'.format(self.test_func_name, test_name))
            self.assertIs(self.test_func(*test_case['argument']), test_case['response'])

    def test_3_type(self):
        for test_name, test_case in self.test_type.items():
            print('Running {} test_type type: {}'.format(self.test_func_name, test_name))
            self.assertRaises(test_case['response'], self.test_func, *test_case['argument'])


class Test_5_start_at_threshold(unittest.TestCase):
    def setUp(self) -> None:
        print('Test_5')
        self.test_func = cvm.CovidMath.start_at_threshold
        self.test_func_name = 'start_at_threshold'
        self.test_equal = {'test1': {'argument': ([1, 2, 3, 4, 5, 6, 7], 4),
                                     'response': [4, 5, 6, 7]},
                           'test2': {'argument': ([1, 2, 3, 4, 5, 6, 7], 0),
                                     'response': [1, 2, 3, 4, 5, 6, 7]},
                           'test3': {'argument': ([1, 2, 3, 4, 5, 6, 7], 10),
                                     'response': []},
                           'test4': {'argument': ([], 10),
                                     'response': []}}
        self.test_type = {'test1': {'argument': ([1, 2, '3b', 4, 5, 6, 7], 10),
                                    'response': TypeError}}

    def test_1_equal(self):
        for test_name, test_case in self.test_equal.items():
            print('Running {} test_equal type: {}'.format(self.test_func_name, test_name))
            self.assertEqual(self.test_func(*test_case['argument']), test_case['response'])

    def test_2_type(self):
        for test_name, test_case in self.test_type.items():
            print('Running {} test_type type: {}'.format(self.test_func_name, test_name))
            self.assertRaises(test_case['response'], self.test_func, *test_case['argument'])


class Test_6_moving_average(unittest.TestCase):
    def setUp(self) -> None:
        print('Test_6')
        self.test_func = cvm.CovidMath.moving_average
        self.test_func_name = 'moving_average'
        self.test_equal = {'test1': {'argument': ([0, 654, 287, 493, 684, 809, 2651, 588, 2068, 1693], 2),
                                     'response': [0, 327.0, 470.5, 390.0, 588.5, 746.5, 1730.0, 1619.5, 1328.0,
                                                  1880.5]},
                           'test2': {'argument': ([0, 654, 287, 493, 684, 809, 2651, 588, 2068, 1693], 3),
                                     'response': [0, 327.0, 313.67, 478.0, 488.0, 662.0, 1381.33, 1349.33, 1769.0,
                                                  1449.67]},
                           'test3': {'argument': ([2068, 1693], 3),
                                     'response': [2068, 1880.5]},
                           'test4': {'argument': ([1693], 3),
                                     'response': [1693]},
                           'test5': {'argument': ([], 3),
                                     'response': []}}
        self.test_type = {'test1': {'argument': ([0, 654, 287, 493, 684, 809, 2651, 588, 2068, 1693], 'three'),
                                    'response': TypeError}}

    def test_1_equal(self):
        for test_name, test_case in self.test_equal.items():
            print('Running {} test_equal type: {}'.format(self.test_func_name, test_name))
            self.assertEqual(round_list(self.test_func(*test_case['argument']), 2),
                             round_list(test_case['response'], 2))

    def test_2_type(self):
        for test_name, test_case in self.test_type.items():
            print('Running {} test_type type: {}'.format(self.test_func_name, test_name))
            self.assertRaises(test_case['response'], self.test_func, *test_case['argument'])


class Test_7_total_to_increment(unittest.TestCase):
    def setUp(self) -> None:
        print('Test_7')
        self.test_func = cvm.CovidMath.total_to_increment
        self.test_func_name = 'total_to_increment'
        self.test_equal = {'test1': {'argument': ([0, 654, 941, 1434, 2118, 2927, 5578, 6166, 8234, 9927]),
                                     'response': [np.nan, 654, 287, 493, 684, 809, 2651, 588, 2068, 1693]},
                           'test2': {'argument': ([0, 654, 941, 1434, 2118, 2000, 5578, 6166, 8234, 9927]),
                                     'response': [np.nan, 654, 287, 493, 684, -118, 3578, 588, 2068, 1693]},
                           'test3': {'argument': ([654]),
                                     'response': [654]},
                           'test4': {'argument': ([]),
                                     'response': []}}
        self.test_type = {'test1': {'argument': ([0, 654, 941, 1434, 2118, 2000, 5578, 6166, '8234', 9927]),
                                    'response': TypeError}}

    def test_1_equal(self):
        for test_name, test_case in self.test_equal.items():
            print('Running {} test_equal type: {}'.format(self.test_func_name, test_name))
            self.assertEqual(self.test_func(test_case['argument']), test_case['response'])

    def test_2_type(self):
        for test_name, test_case in self.test_type.items():
            print('Running {} test_type type: {}'.format(self.test_func_name, test_name))
            self.assertRaises(test_case['response'], self.test_func, test_case['argument'])


if __name__ == "__main__":
    unittest.main()
