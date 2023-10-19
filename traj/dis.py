from math import radians, sin, cos, asin, sqrt
import math


def dis(lon1, lat1, lon2, lat2, geo=True):
    # Check if the coordinates are in geographic format
    if geo is True:
        # Convert the coordinates to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # Calculate the differences in longitude and latitude
        d_lon = lon2 - lon1
        d_lat = lat2 - lat1

        # Apply the Haversine formula to calculate the great circle distance
        aa = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
        c = 2 * asin(sqrt(aa))
        r = 6371  # Earth's radius in kilometers

        # Calculate the distance in meters
        dis = c * r * 1000
    else:
        # Calculate the Euclidean distance between the coordinates
        dis = math.sqrt(abs(lon1 - lon2) ** 2 + abs(lat1 - lat2) ** 2)

    return dis
