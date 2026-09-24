# NMEA PVT Solver

A Python tool that decodes NMEA GPS/GNSS data and computes receiver position using satellite trilateration.

## About

During my internship at **ISRO's Master Control Facility, Hassan**, I worked with an IFEN GNSS receiver tracking NavIC/IRNSS and GPS signals, using Python to decode the receiver's NMEA output and compute Position, Velocity, and Time (PVT). This project rebuilds that pipeline from scratch using public standards (NMEA 0183) — no proprietary code or data.

## How it works

GNSS Satellites (NavIC / GPS)

        ↓
        
Receiver acquires & tracks signals

        ↓
        
Receiver outputs NMEA sentences

        ↓
        
Python parses the NMEA data

        ↓
        
Extracts Latitude / Longitude / Altitude / Time

        ↓
        
Trilateration solves receiver position

        ↓
        
Displays results

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
- 
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
