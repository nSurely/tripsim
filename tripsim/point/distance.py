import enum
import math


class DistanceUnit(str, enum.Enum):
    "Distance unit"
    METERS = 'm'
    KILOMETERS = 'km'
    MILES = 'mi'
    NAUTICAL_MILES = 'nm'


def convert_units(value: float, input_unit: DistanceUnit, output_unit: DistanceUnit) -> float:
    "Converts a distance value from one unit to another"
    if input_unit == output_unit:
        return value
    if input_unit == DistanceUnit.METERS:
        if output_unit == DistanceUnit.KILOMETERS:
            return value / 1000
        if output_unit == DistanceUnit.MILES:
            return value / 1609.344
        if output_unit == DistanceUnit.NAUTICAL_MILES:
            return value / 1852
    if input_unit == DistanceUnit.KILOMETERS:
        if output_unit == DistanceUnit.METERS:
            return value * 1000
        if output_unit == DistanceUnit.MILES:
            return value * 0.621371
        if output_unit == DistanceUnit.NAUTICAL_MILES:
            return value * 0.539957
    if input_unit == DistanceUnit.MILES:
        if output_unit == DistanceUnit.METERS:
            return value * 1609.344
        if output_unit == DistanceUnit.KILOMETERS:
            return value * 1.609344
        if output_unit == DistanceUnit.NAUTICAL_MILES:
            return value * 0.868976
    if input_unit == DistanceUnit.NAUTICAL_MILES:
        if output_unit == DistanceUnit.METERS:
            return value * 1852
        if output_unit == DistanceUnit.KILOMETERS:
            return value * 1.852
        if output_unit == DistanceUnit.MILES:
            return value * 1.15078
    raise ValueError(f'Unknown unit: {input_unit}')


def haversine(lat1, lon1, lat2, lon2):
    "Returns the distance between two points in kilometers"
    R = 6372.8
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat / 2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dLon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c
