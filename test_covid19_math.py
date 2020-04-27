"""Test suite to accompany color_tiles.py"""

import unittest
import numpy as np
import covid19_math as cvm


class Test_0_series_rolling_doubling_time(unittest.TestCase):
    def setUp(self) -> None:
        self.test_equal = {'test1': {'expr': cvm.CovidMath.series_rolling_doubling_time(
                                                 [200, 239, 267, 314, 314, 559, 689, 886, 1058, 1243, 1486,
                                                  1795, 2257, 2815, 3401, 3743, 4269, 4937, 6235, 7284,
                                                  9134, 10836, 11899], 5),
                                     'response': [np.nan, 7.78, 7.2, 6.15, 7.68, 4.08, 3.66, 3.34, 2.85, 4.34,
                                                  4.51, 4.91, 4.57, 4.24, 4.19, 4.72, 5.44, 6.17, 5.72, 5.21,
                                                  4.56, 4.41, 5.36]
                                     },
                           'test2': {'expr': cvm.CovidMath.series_rolling_doubling_time(
                                                 [200.0, 239.0, 267.0, 314.0, 314.0, 559.0, 689.0, 886.0, 1058.0,
                                                  1243.0], 5),
                                     'response': [np.nan, 7.78, 7.2, 6.15, 7.68, 4.08, 3.66, 3.34, 2.85, 4.34]
                                     },
                           'test3': {'expr': cvm.CovidMath.series_rolling_doubling_time(
                                                 [200, 239, 267, 314, 314, 559, 689, 886], 5),
                                     'response': [np.nan, 7.78, 7.2, 6.15, 7.68, 4.08, 3.66, 3.34]
                                     },
                           'test4': {'expr': cvm.CovidMath.series_rolling_doubling_time(
                                                 [np.nan, 239, 267, 314, 314, 559, 689, 886, 1058, 1243, 1486, 1795,
                                                  2257, 2815, 3401, 3743, 4269, 4937, 6235, 7284, 9134, 10836, 11899], 5
                                                  ),
                                     'response': [np.nan, np.nan, 12.51, 7.62, 10.16, 4.08, 3.66, 3.34, 2.85, 4.34, 4.51,
                                                  4.91, 4.57, 4.24, 4.19, 4.72, 5.44, 6.17, 5.72, 5.21, 4.56, 4.41, 5.36
                                                  ]
                                     },
                           'test5': {'expr': cvm.CovidMath.series_rolling_doubling_time(
                                                 [239, 267], 5),
                                     'response': [np.nan, 12.51]
                                     },
                           'test6': {'expr': cvm.CovidMath.series_rolling_doubling_time(
                                                 [239], 5),
                                     'response': [np.nan]
                                     },
                           'test7': {'expr': cvm.CovidMath.series_rolling_doubling_time(
                                                 [], 5),
                                     'response': [np.nan]

                                     }}

        self.test_value = {'test1': {'expr': cvm.CovidMath.series_rolling_doubling_time(
                                                 [200, '239b', 267, 314, 314, 559, 689, '886b'], 5),
                                     'response': TypeError}}

    def test_1_equal(self):
        for test_name, test_case in self.test_equal.items():
            print('Running test equals: {}'.format(test_name))
            self.assertEqual(test_case['expr'], test_case['response'])

    def test_2_value(self):
        for test_name, test_case in self.test_value.items():
            print('Running test value: {}'.format(test_name))
            self.assertRaises(test_case['response'], test_case['expr'])


if __name__ == "__main__":
    unittest.main()
