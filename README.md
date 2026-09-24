# NMEA PVT Solver

A Python tool that decodes NMEA GPS/GNSS data and computes receiver position using satellite trilateration.

## About

During my internship at **ISRO's Master Control Facility, Hassan**, I worked with an IFEN GNSS receiver tracking NavIC/IRNSS and GPS signals, using Python to decode the receiver's NMEA output and compute Position, Velocity, and Time (PVT). This project rebuilds that pipeline from scratch using public standards (NMEA 0183) — no proprietary code or data.

## Example NMEA Sentence

This is a real NMEA $GPGGA sentence, as output by a GNSS receiver:


$GPGGA,123519.00,1258.1234,N,07735.5678,E,1,08,0.8,920.4,M,0.0,M,,*5E


Breaking it down:
| Field | Value | Meaning |
|---|---|---|
| Sentence ID | GPGGA | GPS fix data |
| UTC Time | 123519.00 | 12:35:19 UTC |
| Latitude | 1258.1234,N | 12° 58.1234′ N |
| Longitude | 07735.5678,E | 77° 35.5678′ E |
| Fix Quality | 1 | GPS fix |
| Satellites Used | 08 | 8 satellites |
| Altitude | 920.4,M | 920.4 meters |
| Checksum | *5E | For error checking |

This script reads a sentence like this, verifies its checksum, and decodes each field into a clean, human-readable output.

## How it works

1. GNSS satellites (NavIC / GPS) broadcast signal

2. Receiver acquires and tracks those signals
 
3. Receiver outputs NMEA sentences over its serial port
 
4. Python parses the NMEA data
 
5. Extracts latitude, longitude, altitude, and time
 
6. Trilateration solves the receiver position
 
7. Results are displayed


## Features

- NMEA `$GPGGA` sentence parsing with checksum verification
  
- NMEA coordinate format → decimal degrees conversion
 
- ECEF (Earth-Centered Earth-Fixed) coordinate conversion
  
- Iterative least-squares trilateration solver
  
- Receiver clock-bias estimation
 
- Clean, labeled output

## Sample Output

## NMEA Navigation Data

UTC Time : 12:35:19

Latitude : 12.968723333333333

Longitude : 77.59279666666667

Altitude : 920.4 meters

Satellites : 8

Fix Quality: 1

## Trilateration Demo

Estimated Latitude : 12.968700

Estimated Longitude: 77.592800

Estimated Altitude : 920.0 meters

## Tech Stack

- Python 3
  
- NumPy — matrix math for the trilateration solver

## Getting Started

bash:

pip install numpy

python nmea_pvt.py


## Notes

Satellite positions used in the trilateration demo are illustrative, not real ephemeris data. This project demonstrates the decoding + position-solving pipeline used by real GNSS receivers(IFEN-RECIVER), not a live navigation system.

## Author

**Shreevathsa A P**
• LinkedIn:https://www.linkedin.com/in/shreevathsa-ap-84114526a 

• GitHub:https://github.com/Shreevathsa-Patla
