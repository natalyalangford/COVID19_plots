"""Test suite to accompany color_tiles.py"""

import unittest
import covid19_math


class Test_series_rolling_doubling_time(self):

    def setUp(self) -> None:
        self.testcases = [200, 239, 267, 314, 314, 559, 689, 886, 1058, 1243, 1486, 1795, 2257, 2815,
                   3401, 3743, 4269, 4937, 6235, 7284, 9134, 10836, 11899], 5
        [nan, 7.78, 7.2, 6.15, 7.68, 4.08, 3.66, 3.34, 2.85, 4.34, 4.51, 4.91, 4.57, 4.24, 4.19,
        4.72, 5.44, 6.17, 5.72, 5.21, 4.56, 4.41, 5.36]

class Test_0_Tile(unittest.TestCase):
    """Tests of the Tile class alone"""
    def setUp(self) -> None:
        self.t1 = Tile(Color.red)
        self.t2 = Tile(Color.blue)
        self.t3 = Tile(Color.red)
        self.t4 = Tile(Color.blue)

    def test_0_str(self):
        """Abbreviated tile names: First letter of color"""
        self.assertEqual(str(self.t1), "r")
        self.assertEqual(str(self.t2), "b")

    def test_1_eq(self):
        """Tiles of the same color are equal"""
        self.assertEqual(self.t1,self.t3)
        self.assertEqual(self.t2,self.t4)

    def test_2_neq(self):
        """Tiles of different colors are not equal"""
        self.assertNotEqual(self.t1,self.t2)
        self.assertNotEqual(self.t3,self.t4)


class Test_1_Row(unittest.TestCase):

    def setUp(self) -> None:
        self.r0 = Row()   # Empty row
        self.r1 = Row()   # Row built up with 'append'
        self.r1.append(Tile(Color.red))
        self.r1.append(Tile(Color.red))
        self.r1.append(Tile(Color.blue))
        self.r1.append(Tile(Color.blue))
        # Identical row built from string
        self.r2 = Row()
        self.r2.append("b")  # This should be overridden
        self.r2.from_abbreviation("rrbb")
        # Row with different tile colors
        self.r3 = Row()
        self.r3.from_abbreviation("rbbr")
        # Row with different number of tiles
        self.r4 = Row()
        self.r4.from_abbreviation("rrb")
        # Another empty row
        self.r5 = Row()

    def test_1_str(self):
        self.assertEqual(str(self.r0), "")
        self.assertEqual(str(self.r1), "rrbb")
        self.assertEqual(str(self.r2), "rrbb")
        self.assertEqual(str(self.r3), "rbbr")
        self.assertEqual(str(self.r4), "rrb")

    def test_2_eq(self):
        self.assertEqual(self.r1, self.r2)
        self.assertEqual(self.r0, self.r5)

    def test_3_neq(self):
        self.assertNotEqual(self.r0, self.r1)
        self.assertNotEqual(self.r1, self.r0)
        self.assertNotEqual(self.r1, self.r3)
        self.assertNotEqual(self.r3, self.r4)
        self.assertNotEqual(self.r4, self.r3)


if __name__ == "__main__":
    unittest.main()
