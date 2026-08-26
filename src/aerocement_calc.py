#!/usr/bin/env python3
"""aerocement-calc — offline-first appropriate-technology calculator.

Core calculations for AeroCement / passive solar-thermal work.
Pure stdlib. Runs on Termux and low-resource devices.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Optional


DEFAULT_IRRADIANCE = 931.0
DEFAULT_AEROCEMENT_DENSITY = 0.55
DEFAULT_SPECIFIC_HEAT = 880.0


@dataclass
class SolarResult:
    area_m2: float
    irradiance_w_m2: float
    hours: float
    instant_power_w: float
    daily_energy_kwh: float

    def report(self) -> str:
        return (
            f"Solar capture estimate\n"
            f"  Area:          {self.area_m2:8.2f} m²\n"
            f"  Irradiance:    {self.irradiance_w_m2:8.2f} W/m²\n"
            f"  Hours:         {self.hours:8.2f} h\n"
            f"  Instant power: {self.instant_power_w:8.2f} W\n"
            f"  Daily energy:  {self.daily_energy_kwh:8.2f} kWh"
        )


@dataclass
class MaterialResult:
    volume_m3: float
    density: float
    mass_kg: float

    def report(self) -> str:
        return (
            f"Material quantity estimate\n"
            f"  Volume:  {self.volume_m3:8.3f} m³\n"
            f"  Density: {self.density:8.3f} (relative)\n"
            f"  Mass:    {self.mass_kg:8.1f} kg"
        )


@dataclass
class ThermalResult:
    mass_kg: float
    delta_t_k: float
    energy_kj: float
    energy_kwh: float

    def report(self) -> str:
        return (
            f"Thermal mass estimate\n"
            f"  Mass:     {self.mass_kg:8.1f} kg\n"
            f"  ΔT:       {self.delta_t_k:8.1f} K\n"
            f"  Energy:   {self.energy_kj:8.1f} kJ  ({self.energy_kwh:6.3f} kWh)"
        )


def calc_solar(area: float, irradiance: float = DEFAULT_IRRADIANCE, hours: float = 5.0) -> SolarResult:
    power = area * irradiance
    energy = power * hours / 1000.0
    return SolarResult(area, irradiance, hours, power, energy)


def calc_material(volume: float, density: float = DEFAULT_AEROCEMENT_DENSITY) -> MaterialResult:
    mass = volume * density * 1000.0
    return MaterialResult(volume, density, mass)


def calc_thermal(mass: float, delta_t: float, specific_heat: float = DEFAULT_SPECIFIC_HEAT) -> ThermalResult:
    energy_j = mass * specific_heat * delta_t
    energy_kj = energy_j / 1000.0
    energy_kwh = energy_j / 3_600_000.0
    return ThermalResult(mass, delta_t, energy_kj, energy_kwh)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="aerocement-calc",
        description="Offline-first AeroCement / appropriate-technology calculator",
    )
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("solar", help="Solar capture estimate")
    s.add_argument("--area", type=float, required=True, help="Collector area in m²")
    s.add_argument("--irradiance", type=float, default=DEFAULT_IRRADIANCE, help="W/m²")
    s.add_argument("--hours", type=float, default=5.0, help="Effective hours")

    m = sub.add_parser("material", help="Material quantity for volumetric aerocement")
    m.add_argument("--volume", type=float, required=True, help="Volume in m³")
    m.add_argument("--density", type=float, default=DEFAULT_AEROCEMENT_DENSITY, help="Relative density")

    t = sub.add_parser("thermal", help="Thermal mass energy storage")
    t.add_argument("--mass", type=float, required=True, help="Mass in kg")
    t.add_argument("--delta-t", type=float, required=True, help="Temperature rise in K")
    t.add_argument("--cp", type=float, default=DEFAULT_SPECIFIC_HEAT, help="Specific heat J/(kg·K)")

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "solar":
        result = calc_solar(args.area, args.irradiance, args.hours)
        print(result.report())
    elif args.command == "material":
        result = calc_material(args.volume, args.density)
        print(result.report())
    elif args.command == "thermal":
        result = calc_thermal(args.mass, args.delta_t, args.cp)
        print(result.report())
    else:
        parser.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
