import numpy as np
import math
from pyproj import Transformer
from math import radians, sin, cos, asin, sqrt

def xy_trans(x, y, azimuth, distance, point=False):
    # Calculate the new x and y coordinates based on the given azimuth and distance
    x1 = x + distance * math.cos(math.radians(azimuth))
    y1 = y + distance * math.sin(math.radians(azimuth))

    # Check if the 'point' parameter is True
    if point is True:
        # If True, return the coordinates as a tuple
        return (x1, y1)
    else:
        # If False, return the coordinates as separate values
        return (x1, y1)[0], (x1, y1)[1]





def geo_xy_changer(lon=None, lat=None, x=None, y=None, ref_lat=39.85183, ref_lon=116.69176, geo_to_xy=True):
    # Check if the conversion is from geographic coordinates to xy coordinates
    if geo_to_xy is True:
        # Convert the latitude and longitude values to radians
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        ref_lat_rad = math.radians(ref_lat)
        ref_lon_rad = math.radians(ref_lon)

        # Calculate trigonometric values for the conversion
        sin_lat = math.sin(lat_rad)
        cos_lat = math.cos(lat_rad)
        ref_sin_lat = math.sin(ref_lat_rad)
        ref_cos_lat = math.cos(ref_lat_rad)
        cos_d_lon = math.cos(lon_rad - ref_lon_rad)

        # Calculate the new x and y coordinates
        arg = np.clip(ref_sin_lat * sin_lat + ref_cos_lat * cos_lat * cos_d_lon, -1.0, 1.0)
        c = math.acos(arg)
        k = 1.0

        if abs(c) > 0:
            k = (c / math.sin(c))
            x1 = float(k * (ref_cos_lat * sin_lat - ref_sin_lat * cos_lat * cos_d_lon) * 6371000)
            y1 = float(k * cos_lat * math.sin(lon_rad - ref_lon_rad) * 6371000)

        return x1, y1
    else:
        # Convert the xy coordinates to geographic coordinates
        x_rad = float(x) / 6371000
        y_rad = float(y) / 6371000
        c = math.sqrt(x_rad * x_rad + y_rad * y_rad)

        ref_lat_rad = math.radians(ref_lat)
        ref_lon_rad = math.radians(ref_lon)
        ref_sin_lat = math.sin(ref_lat_rad)
        ref_cos_lat = math.cos(ref_lat_rad)

        if abs(c) > 0:
            sin_c = math.sin(c)
            cos_c = math.cos(c)

            lat_rad = math.asin(cos_c * ref_sin_lat + (x_rad * sin_c * ref_cos_lat) / c)
            lon_rad = (ref_lon_rad + math.atan2(y_rad * sin_c, c * ref_cos_lat * cos_c - x_rad * ref_sin_lat * sin_c))

            lat1 = math.degrees(lat_rad)
            lon1 = math.degrees(lon_rad)
        else:
            lat1 = math.degrees(ref_lat)
            lon1 = math.degrees(ref_lon)

        # Check if the xy coordinates are (0, 0)
        if x == 0.0 and y == 0.0:
            # If True, return the reference longitude and latitude
            return ref_lon, ref_lat
        else:
            # If False, return the converted longitude and latitude
            return lon1, lat1


def crs_changer(x, y, src_crs, dst_crs, point=True):
    # Create a transformer object to convert coordinates between different coordinate reference systems (CRS)
    transformer = Transformer.from_crs(src_crs, dst_crs, always_xy=True)

    # Transform the x and y coordinates from the source CRS to the destination CRS
    lon, lat = transformer.transform(x, y)

    # Check if the 'point' parameter is True
    if point is True:
        # If True, return the coordinates as a tuple
        return (lon, lat)
    else:
        # If False, return the coordinates as separate values
        return (lon, lat)[0], (lon, lat)[1]
