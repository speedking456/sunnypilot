#!/usr/bin/env python3
# The MIT License
#
# Copyright (c) 2019-, Rick Lan, dragonpilot community, and a number of other of contributors.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Last updated: August 12, 2024

from cereal import custom
from openpilot.common.numpy_fast import interp

AccelPersonality = custom.AccelerationPersonality

# accel personality by @arne182 modified by cgw and kumar
#_DP_CRUISE_MIN_V =       [-1.0,  -1.0]
#_DP_CRUISE_MIN_V_ECO =   [-1.0,  -1.0]
#_DP_CRUISE_MIN_V_SPORT = [-1.0,  -1.0]
#_DP_CRUISE_MIN_BP =      [0.,    40.]

_DP_CRUISE_MIN_V =       [-0.031, -0.031, -0.011, -0.011, -0.11, -0.11, -0.33, -0.33, -0.63, -0.63, -0.79, -0.79, -1.0,  -1.0]
_DP_CRUISE_MIN_V_ECO =   [-0.030, -0.030, -0.010, -0.010, -0.10, -0.10, -0.32, -0.32, -0.64, -0.64, -0.78, -0.78, -1.0,  -1.0]
_DP_CRUISE_MIN_V_SPORT = [-0.032, -0.032, -0.012, -0.012, -0.12, -0.12, -0.34, -0.34, -0.66, -0.66, -0.80, -0.80, -1.0,  -1.0]
_DP_CRUISE_MIN_BP =      [0.,     3.0,    3.01,   8.0,    8.01,  12.,   12.01, 16.,   16.01, 20.,   20.01,  25.,  25.01, 30.]

_DP_CRUISE_MAX_V =       [2.0, 2.0, 2.0, 1.70, 1.30, .66,  .54,  .38,  .17]
_DP_CRUISE_MAX_V_ECO =   [2.0, 2.0, 2.0, 1.40, 1.00, .58,  .46,  .32,  .09]
_DP_CRUISE_MAX_V_SPORT = [2.0, 2.0, 2.0, 2.00, 1.63, .84,  .70,  .50,  .30]
_DP_CRUISE_MAX_BP =      [0.,  4.,  6.,  8.,   11.,  20.,  25.,  30.,  40.]



class AccelController:
  def __init__(self):
    self._personality = AccelPersonality.stock

  def _dp_calc_cruise_accel_limits(self, v_ego: float) -> tuple[float, float]:
    if self._personality == AccelPersonality.eco:
      min_v = _DP_CRUISE_MIN_V_ECO
      max_v = _DP_CRUISE_MAX_V_ECO
    elif self._personality == AccelPersonality.sport:
      min_v = _DP_CRUISE_MIN_V_SPORT
      max_v = _DP_CRUISE_MAX_V_SPORT
    else:
      min_v = _DP_CRUISE_MIN_V
      max_v = _DP_CRUISE_MAX_V

    a_cruise_min = interp(v_ego, _DP_CRUISE_MIN_BP, min_v)
    a_cruise_max = interp(v_ego, _DP_CRUISE_MAX_BP, max_v)

    return a_cruise_min, a_cruise_max

  def get_accel_limits(self, v_ego: float, accel_limits: list[float]) -> tuple[float, float]:
    return accel_limits if self._personality == AccelPersonality.stock else self._dp_calc_cruise_accel_limits(v_ego)

  def is_enabled(self, accel_personality: int = AccelPersonality.stock) -> bool:
    self._personality = accel_personality
    return self._personality != AccelPersonality.stock