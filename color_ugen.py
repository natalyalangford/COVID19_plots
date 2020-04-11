#!/usr/bin/env python3
""" color-ugen  -  ColorUgen Class

    Copyright (C) 2019  RueiKe

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
__author__ = 'RueiKe'
__copyright__ = 'Copyright (C) 2020 RueiKe'
__credits__ = []
__license__ = 'GNU General Public License'
__program_name__ = 'color-pal'
__version__ = 'v0.0.1'
__maintainer__ = 'RueiKe'
__status__ = 'Development'
__docformat__ = 'reStructuredText'
# pylint: disable=multiple-statements
# pylint: disable=line-too-long

import colorsys
import math
from typing import List, Tuple, Union, Dict

ColSpaceVal = Union[List[float], Tuple[float, ...]]
ColSpaceList = List[float]
ColorDict = Dict[str, ColSpaceList]


class ColorUgen:
    """
    Class for the generation of sets of distinct colors.
    """
    def __init__(self):
        # Key is #rgb, value is source color space, ot yiq if source is rgb
        self.colors: ColorDict = {}
        self.counter = 0
        self.maps = ['rgb', 'hsv']

    def sort_by_key(self) -> None:
        """
        Sort by hex rgb string.  Not sure how useful this is.
        """
        self.colors = {key: self.colors[key] for key in sorted(self.colors.keys())}

    def sort_by_value(self) -> None:
        """
        Sort by value, use correct value tuple index based on color space.
        """
        tup_val = 0 if self.maps[1] == 'yiq' else 2
        self.colors = {k: v for k, v in sorted(self.colors.items(), key=lambda x: x[1][tup_val], reverse=True)}

    def drop_bright(self, y: float = 1.0) -> None:
        """
        Drop color items from list based on high brightness (v for hsv and y for yiq)

        :param y: brightness 0-1
        """
        if y >= 1.0: return
        tup_val = 0 if self.maps[1] == 'yiq' else 2
        self.colors = {k: v for k, v in self.colors.items() if v[tup_val] < y}

    def drop_dark(self, y: float = 0.0) -> None:
        """
        Drop color items from list based on low brightness (v for hsv and y for yiq)

        :param y: brightness 0-1
        """
        if y <= 0.0: return
        tup_val = 0 if self.maps[1] == 'yiq' else 2
        self.colors = {k: v for k, v in self.colors.items() if v[tup_val] > y}

    def add_rgb(self, add_val: ColSpaceVal, color_space: str = 'hsv', quiet: bool = True) -> None:
        """
        Add new color to color dictionary. Key will be hex rgb string, value will be original color
        map value or yiq if orig is rgb.

        :param add_val: Three element tuple of color in given color space.
        :param color_space: Name of color space used to generate colors.
        :param quiet: More output if True
        """
        if color_space == 'yiq':
            rgb_tup = colorsys.yiq_to_rgb(*add_val)
            self.maps[1] = 'yiq'
        elif color_space == 'rgb':
            rgb_tup = add_val
            add_val = colorsys.rgb_to_yiq(*add_val)
            self.maps[1] = 'yiq'
        else:
            rgb_tup = colorsys.hsv_to_rgb(*add_val)
            self.maps[1] = 'hsv'

        if rgb_tup[0] < 0 or rgb_tup[1] < 0 or rgb_tup[2] < 0:
            print('RGB error: {}'.format(rgb_tup))
            return

        hex_rgb = '#{:02x}{:02x}{:02x}'.format(int(rgb_tup[0]*255), int(rgb_tup[1]*255), int(rgb_tup[2]*255))
        if not quiet:
            print('rgb: {}, {}: ({:.2f}, {:.2f}, {:.2f})'.format(hex_rgb, self.maps[1], *add_val))
        self.colors.update({hex_rgb: add_val})
        self.counter += 1
        return

    def color_gen_list(self, num_cols: int, color_space: str = 'hsv', debug: bool = False):
        """
        Generate a minimum number of colors by stepping through the given color space.

        :param num_cols: Minimum number of colors to generate.
        :param color_space: Source color space
        :param debug: More debug info displayed if True
        :return: List of colors as hex rgb strings
        """
        if color_space == 'yiq':
            return self.color_gen_list_from_yiq(num_cols, debug)
        elif color_space == 'rgb':
            return self.color_gen_list_from_rgb(num_cols, debug)
        return self.color_gen_list_from_hsv(num_cols, debug)

    def color_gen_list_from_rgb(self, num_cols: int, debug: bool = False) -> List[str]:
        """
        Generate a list of color from the rgb color cube and return a list greater in length than num_cols.

        :param num_cols: Minimum number of colors to generate.
        :param debug: More debug info displayed if True
        :return: List of colors as hex rgb strings
        """
        # Calculate optimal number of steps for num_cols distinct colors
        size_side = int((num_cols ** (1.0/3.0)) // 1)
        num_r = num_g = num_b = size_side + 1
        if debug: print('loops: r={}, g={}, b={}'.format(num_r, num_g, num_b))

        # Calculate range parameters, start, stop, index.  Subtract from hue stop, to allow drifting start
        r_params = (0, 255, num_r)  # min, max, num_steps
        g_params = (0, 255, num_g)
        b_params = (0, 255, num_b)
        if debug: print('params: r={}, g={}, b={}'.format(r_params, g_params, b_params))

        # Set parameters for jittering iqx and iqy values between y steps.

        # Set step sizes, always round up
        r_step = int(((r_params[1] - r_params[0]) / r_params[2]) // 1) + 1
        g_step = int(((g_params[1] - g_params[0]) / g_params[2]) // 1) + 1
        b_step = int(((b_params[1] - b_params[0]) / b_params[2]) // 1) + 1
        if debug: print('r_step: {}, g_step: {}, b_step: {}'.format(r_step, g_step, b_step))

        # Step through RGB values
        for t_r in range(r_params[0], r_params[1], r_step):
            for t_b in range(b_params[0], b_params[1], b_step):
                for t_g in range(g_params[0], g_params[1], g_step):
                    self.add_rgb(tuple([t_r/255, t_g/255, t_b/255]), color_space='rgb')

        self.drop_bright(0.6)
        self.drop_dark(0.2)
        self.sort_by_value()
        return list(self.colors.keys())

    def color_gen_list_from_yiq(self, num_cols: int, debug: bool = False) -> List[str]:
        """
        Generate a list of color from the yiq color space and return a list greater in length than num_cols.

        :param num_cols: Minimum number of colors to generate.
        :param debug: More debug info displayed if True
        :return: List of colors as hex rgb strings
        ..note:: Stepping through the space is probably not correct.
        """
        # TODO = need to step through z, x, y of the cube in the y, i, q space and translate to y, i, q coords.
        # Calculate optimal number of steps for num_cols distinct colors
        num_iqx = 5
        num_iqy = 5
        num_y = int(num_cols / (num_iqx * num_iqy))
        if debug: print('loops: y={}, iqx={}, iqy={}'.format(num_y, num_iqx, num_iqy))

        # Calculate range parameters, start, stop, index.  Subtract from hue stop, to allow drifting start
        y_params = (10, 90, num_y)  # min, max, num_steps
        iqx_params = (-100, 100, num_iqx)
        iqy_params = (-100, 100, num_iqy)
        if debug: print('params: y={}, iqx={}, iqy={}'.format(y_params, iqx_params, iqy_params))

        # Set parameters for jittering iqx and iqy values between y steps.

        # Set step sizes, always round up
        y_step = int(((y_params[1] - y_params[0]) / y_params[2]) // 1) + 1
        iqx_step = int(((iqx_params[1] - iqx_params[0]) / iqx_params[2]) // 1) + 1
        iqy_step = int(((iqy_params[1] - iqy_params[0]) / iqy_params[2]) // 1) + 1
        if debug: print('y_step: {}, iqx_step: {}, iqy_step: {}'.format(y_step, iqx_step, iqy_step))

        # This doesn't work, as the color cube is rotated -33deg about the y axis and scaled.
        # https://hbfs.wordpress.com/2018/05/08/yuv-and-yiq-colorspaces-v/
        # Step from brightest to darkest
        for t_y in range(y_params[1], y_params[0], -y_step):
            yiq_y = t_y / 100

            # Step from lowest to highest iqx
            for t_iqx in range(iqx_params[0], iqx_params[1], iqx_step):
                yiq_iqx = t_iqx / 100

                # Step from lowest to highest iqy
                for t_iqy in range(iqy_params[0], iqy_params[1], iqy_step):
                    yiq_iqy = t_iqy / 100
                    self.add_rgb(tuple([yiq_y, yiq_iqx, yiq_iqy]), color_space='yiq')

        return list(self.colors.keys())

    def color_gen_list_from_hsv(self, num_cols: int, debug: bool = False) -> List[str]:
        """
        Generate a list of color from the hsv color cylinder and return a list greater in length than num_cols.

        :param num_cols: Minimum number of colors to generate.
        :param debug: More debug info displayed if True
        :return: List of colors as hex rgb strings
        """

        # Calculate optimal number of steps for num_cols distinct colors
        num_hues = 18
        num_vals = num_sats = int((math.sqrt(num_cols/num_hues)) // 1) + 1
        if num_cols > 90:
            if num_hues * num_sats * num_vals > 1.2 * num_cols: num_hues -= 1
        else:
            num_hues -= 1
            num_sats += 1
        if debug: print('loops: h={}, s={}, v={}'.format(num_hues, num_sats, num_vals))

        # Calculate range parameters, start, stop, index.  Subtract from hue stop, to allow drifting start
        max_hue = 3600 - int(3600/num_hues)
        h_params = (0, max_hue, num_hues)  # min, max, num_steps
        s_params = (40, 90, num_sats)
        v_params = (40, 80, num_vals)
        if debug: print('params: h={}, s={}, v={}'.format(h_params, s_params, v_params))

        # Set parameters for drifting hue
        total_sv_steps = s_params[2] * v_params[2]
        start_hue = h_params[0]

        # Set step sizes, always round up
        v_step = int(((v_params[1] - v_params[0]) / v_params[2]) // 1) + 1
        s_step = int(((s_params[1] - s_params[0]) / s_params[2]) // 1) + 1
        h_step = int(((h_params[1] - h_params[0]) / h_params[2]) // 1) + 1
        if debug: print('h_step: {}, v_step: {}, s_step: {}'.format(h_step, v_step, s_step))

        # Step from brightest to darkest
        for t_val in range(v_params[1], v_params[0], -v_step):
            hsv_val = t_val / 100.0

            # Step from highest saturation to lowest
            for t_sat in range(s_params[1], s_params[0], -s_step):
                hsv_sat = t_sat / 100.0

                # Step from red to one step before red again
                for t_hue in range(h_params[0] + start_hue, h_params[1] + start_hue, h_step):
                    # Green correct 120
                    if 800 < t_hue < 1100 or 1300 < t_hue < 1600: continue
                    if hsv_val > 0.70:
                        m_hsv_val = hsv_val * 0.95 if 500 < t_hue < 1800 else hsv_val
                    else:
                        m_hsv_val = hsv_val
                    # End Green correct
                    hsv_hue = float(t_hue) / 3600.0
                    self.add_rgb(tuple([hsv_hue, hsv_sat, m_hsv_val]), color_space='hsv')
                start_hue += int(h_step / total_sv_steps)
                if debug: print('start_hue: {}'.format(start_hue))
        return list(self.colors.keys())

    def print(self) -> None:
        """
        Print the color dictionary.
        """
        print('Added hsv: {}, Resultant rgb: {}'.format(self.counter, len(self.colors)))
        for rgb, ocm in self.colors.items():
            print('rgb: {}, {}: ({:.2f}, {:.2f}, {:.2f})'.format(rgb, self.maps[1], *ocm))
