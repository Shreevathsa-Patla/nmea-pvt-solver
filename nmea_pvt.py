# nmea_pvt.py - Reads NMEA GPS data and computes position using trilateration

import numpy as np


def verify_checksum(sentence):
    sentence = sentence.strip()
    if not sentence.startswith("$") or "*" not in sentence:
        return False
    payload, _, checksum_str = sentence[1:].partition("*")
    checksum = 0
    for ch in payload:
        checksum ^= ord(ch)
    try:
        return checksum == int(checksum_str[:2], 16)
    except ValueError:
        return False


def nmea_to_decimal(raw, hemisphere, is_lon=False):
    if not raw:
        return None
    deg_len = 3 if is_lon else 2
    deg = int(raw[:deg_len])
    minutes = float(raw[deg_len:])
    value = deg + minutes / 60
    return -value if hemisphere in ("S", "W") else value


def parse_gga(line):
    if not verify_checksum(line):
        return None
    fields = line.split("*")[0].split(",")
    if fields[0][-3:] != "GGA":
        return None
    return {
        "utc_time": fields[1],
        "latitude": nmea_to_decimal(fields[2], fields[3]),
        "longitude": nmea_to_decimal(fields[4], fields[5], is_lon=True),
        "fix_quality": int(fields[6]) if fields[6] else 0,
        "num_satellites": int(fields[7]) if fields[7] else 0,
        "altitude": float(fields[9]) if fields[9] else None,
    }


def format_time(raw):
    return f"{raw[0:2]}:{raw[2:4]}:{raw[4:6]}" if raw and len(raw) >= 6 else raw


def print_fix(fix):
    print("----- NMEA Navigation Data -----")
    print(f"UTC Time : {format_time(fix['utc_time'])}")
    print(f"Latitude : {fix['latitude']}")
    print(f"Longitude : {fix['longitude']}")
    print(f"Altitude : {fix['altitude']} meters")
    print(f"Satellites : {fix['num_satellites']}")
    print(f"Fix Quality: {fix['fix_quality']}")


# convert latitude/longitude/altitude to ECEF coordinates
def lla_to_ecef(lat_deg, lon_deg, alt_km=0.0):
    R = 6378.137
    lat, lon = np.radians(lat_deg), np.radians(lon_deg)
    x = (R + alt_km) * np.cos(lat) * np.cos(lon)
    y = (R + alt_km) * np.cos(lat) * np.sin(lon)
    z = (R + alt_km) * np.sin(lat)
    return np.array([x, y, z])


# solve receiver position from satellite positions and pseudoranges
def solve_position(sat_positions, pseudoranges, max_iter=15):
    sat_positions = np.array(sat_positions)
    pseudoranges = np.array(pseudoranges)
    state = np.array([6378.0, 0.0, 0.0, 0.0])

    for _ in range(max_iter):
        pos = state[:3]
        ranges = np.linalg.norm(sat_positions - pos, axis=1)
        predicted = ranges + state[3]
        residual = pseudoranges - predicted

        los = (pos - sat_positions) / ranges[:, None]
        H = np.hstack([los, np.ones((len(sat_positions), 1))])
        delta, *_ = np.linalg.lstsq(H, residual, rcond=None)
        state += delta

        if np.linalg.norm(delta[:3]) < 1e-6:
            break

    return state[:3], state[3]


# convert ECEF back to latitude/longitude/altitude
def ecef_to_lla(x, y, z):
    R = 6378.137
    lon = np.degrees(np.arctan2(y, x))
    p = np.sqrt(x**2 + y**2)
    lat = np.degrees(np.arctan2(z, p))
    alt = np.sqrt(x**2 + y**2 + z**2) - R
    return lat, lon, alt


if __name__ == "__main__":
    sample_line = "$GPGGA,123519.00,1258.1234,N,07735.5678,E,1,08,0.8,920.4,M,0.0,M,,*5E"

    fix = parse_gga(sample_line)
    if fix:
        print_fix(fix)
    else:
        print("Could not parse this NMEA line (bad checksum or wrong sentence type).")

    # demo: trilateration with 4 example satellite positions + pseudoranges
    print("\n----- Trilateration Demo -----")
    receiver_true = lla_to_ecef(12.9687, 77.5928, 0.92)
    sat_positions = [
        receiver_true + [20000, 5000, 3000],
        receiver_true + [-15000, 12000, 8000],
        receiver_true + [3000, -18000, 15000],
        receiver_true + [10000, 10000, -20000],
    ]
    pseudoranges = [np.linalg.norm(np.array(s) - receiver_true) for s in sat_positions]

    est_pos, clock_bias = solve_position(sat_positions, pseudoranges)
    lat, lon, alt = ecef_to_lla(*est_pos)
    print(f"Estimated Latitude : {lat:.6f}")
    print(f"Estimated Longitude: {lon:.6f}")
    print(f"Estimated Altitude : {alt*1000:.1f} meters")
