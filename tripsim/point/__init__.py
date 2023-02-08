from typing import Tuple
from dataclasses import dataclass, field
import math
from typing import Tuple

from .distance import convert_units, DistanceUnit, haversine


@dataclass
class Point:
    "A point coordinate with a timestamp and meta data"
    lat: float
    lon: float
    timestamp: float = 0.0
    meta: dict = field(default_factory=dict)

    def set_timestamp(self, timestamp: float) -> None:
        self.timestamp = timestamp

    def get_lat(self) -> float:
        return self.lat

    def get_lon(self) -> float:
        return self.lon

    @property
    def x(self) -> float:
        "Returns the longitude"
        return self.lon

    @property
    def y(self) -> float:
        "Returns the latitude"
        return self.lat

    @property
    def xy(self) -> Tuple[float, float]:
        return self.x, self.y

    def add_meta(self, key: str, value: any) -> None:
        "Adds a key value pair to the meta data"
        self.meta[key] = value

    def get_meta(self, key: str, default=None) -> any:
        "Returns the value for the given key"
        return self.meta.get(key, default)

    def bearing_to(self, other: 'Point') -> float:
        "Returns the bearing from this point to the other point in degrees"
        x1, y1 = self.xy
        x2, y2 = other.xy

        y1, x1, y2, x2 = map(math.radians, [y1, x1, y2, x2])
        delta_lon = x2 - x1
        y = math.sin(delta_lon) * math.cos(y2)
        x = math.cos(y1) * math.sin(y2) - math.sin(y1) * \
            math.cos(y2) * math.cos(delta_lon)
        bearing = math.atan2(y, x)
        return math.degrees(bearing)

    def distance_to(self, other: 'Point', unit: DistanceUnit = DistanceUnit.KILOMETERS) -> float:
        "Returns the distance from this point to the other point in km"
        x1, y1 = self.xy
        x2, y2 = other.xy
        return convert_units(
            haversine(y1, x1, y2, x2),
            DistanceUnit.KILOMETERS,
            unit
        )

    def next_point(self, distance: float, bearing: float) -> 'Point':
        "Returns a lat lon point that is distance away from start_coord in the direction of bearing"
        # Calculate the new point
        R = 6378.1
        brng = math.radians(bearing)
        d = distance
        lat1 = math.radians(self.lat)
        lon1 = math.radians(self.lon)
        lat2 = math.asin(math.sin(lat1) * math.cos(d / R) +
                         math.cos(lat1) * math.sin(d / R) * math.cos(brng))
        lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(
            lat1), math.cos(d / R) - math.sin(lat1) * math.sin(lat2))
        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)
        return Point(lat2, lon2)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Point):
            return self.lat == __o.lat and self.lon == __o.lon
        return False

    # make indexable
    def __getitem__(self, key):
        if key == 0:
            return self.lat
        elif key == 1:
            return self.lon
        else:
            raise IndexError

    def as_tuple(self):
        "Returns the point as a tuple, in the format (lat, lon) [(y, x)]"
        return (self.lat, self.lon)
