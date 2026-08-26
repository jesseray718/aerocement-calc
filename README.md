# aerocement-calc

Offline-first Python CLI for AeroCement / appropriate-technology calculations.

**Problem solved**  
Field and workshop calculations for volumetric aerated cement, passive solar capture, thermal mass, material quantities, and basic energy estimates must be possible without internet, without cloud accounts, and on low-resource devices (Termux on Android, refurbished desktops).

**Who it is for**  
Builders, inventors, and researchers working with open-cell aerated cement, passive solar-thermal systems, and related appropriate technology who need reproducible numbers they can trust and share.

## Features

- Solar capture estimate (W/m² → daily/seasonal energy)
- Material quantity estimator for volumetric aerocement mixes
- Thermal mass and storage volume calculations
- Simple cost and BOM helpers
- Pure Python + stdlib — runs on Termux, OptiPlex, any modern Python 3.8+
- Offline by design

## Requirements

- Python 3.8 or newer
- No external dependencies for core calculator

## Installation

```bash
git clone https://github.com/jesseray718/aerocement-calc.git
cd aerocement-calc
python3 -m pip install -e .   # optional, or just run from src
```

Or run directly:

```bash
python3 src/aerocement_calc.py --help
```

## Usage

```bash
python3 src/aerocement_calc.py solar --area 12 --irradiance 931
python3 src/aerocement_calc.py material --volume 2.5 --density 0.6
python3 src/aerocement_calc.py thermal --mass 1800 --delta-t 15
```

## Example

```bash
$ python3 src/aerocement_calc.py solar --area 10 --irradiance 931 --hours 5
Solar capture estimate
  Area:            10.00 m²
  Irradiance:     931.00 W/m²
  Hours:            5.00 h
  Instant power:  9310.00 W
  Daily energy:   46.55 kWh
```

## Limitations

- Uses simplified constant-irradiance model (no tilt, shading, or weather series yet)
- Material density defaults are approximate; always calibrate with local mixes
- No graphical UI — intentional for offline and low-resource use

## Roadmap

- [ ] Add tilt and orientation factors
- [ ] CSV batch mode for field logs
- [ ] Thermal cascade (Black Locust RMH) coupling
- [ ] Export to simple BOM markdown

## How to contribute

See CONTRIBUTING.md. Small, tested patches preferred. All changes must keep the tool runnable offline with zero new required dependencies unless η-justified.

## License

GPL-3.0-or-later (code)  
Documentation and examples may be dual-licensed under CC-BY-SA-4.0 where noted.
