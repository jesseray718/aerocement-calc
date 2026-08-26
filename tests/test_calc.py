#!/usr/bin/env python3
"""Minimal tests for aerocement-calc. Run with: python3 tests/test_calc.py"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from aerocement_calc import calc_solar, calc_material, calc_thermal


def test_solar_basic():
    r = calc_solar(area=10.0, irradiance=931.0, hours=5.0)
    assert abs(r.instant_power_w - 9310.0) < 0.01
    assert abs(r.daily_energy_kwh - 46.55) < 0.01


def test_material_basic():
    r = calc_material(volume=2.0, density=0.55)
    assert abs(r.mass_kg - 1100.0) < 0.01


def test_thermal_basic():
    r = calc_thermal(mass=1000.0, delta_t=10.0)
    assert abs(r.energy_kj - 8800.0) < 0.1
    assert abs(r.energy_kwh - 2.444) < 0.01


if __name__ == "__main__":
    test_solar_basic()
    test_material_basic()
    test_thermal_basic()
    print("All tests passed.")
