# Example session

```bash
$ python3 src/aerocement_calc.py solar --area 12 --irradiance 931 --hours 4.5
Solar capture estimate
  Area:             12.00 m²
  Irradiance:      931.00 W/m²
  Hours:             4.50 h
  Instant power: 11172.00 W
  Daily energy:     50.27 kWh

$ python3 src/aerocement_calc.py material --volume 1.8 --density 0.52
Material quantity estimate
  Volume:     1.800 m³
  Density:    0.520 (relative)
  Mass:     936.0 kg

$ python3 src/aerocement_calc.py thermal --mass 1800 --delta-t 18
Thermal mass estimate
  Mass:     1800.0 kg
  ΔT:         18.0 K
  Energy:  28512.0 kJ  ( 7.920 kWh)
```
