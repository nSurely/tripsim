from tripsim import Point, simulate_trip
import math


class TestPoints:

    def test_point(self):
        p = Point(1, 2)
        assert p.y == 1
        assert p.x == 2

    def test_point_timestamp(self):
        p = Point(1, 2, timestamp=3)
        assert p.timestamp == 3

        p.set_timestamp(4)
        assert p.timestamp == 4

    def test_point_meta(self):
        p = Point(1, 2, meta={'a': 1})
        assert p.meta == {'a': 1}

        p.add_meta('b', 2)
        assert p.meta == {'a': 1, 'b': 2}

    def test_point_equality(self):
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        assert p1 == p2

    def test_point_inequality(self):
        p1 = Point(1, 2)
        p2 = Point(1, 3)
        assert p1 != p2

    def test_point_distance(self):
        p1 = Point(1, 2)
        p2 = Point(1, 3)
        assert math.isclose(p1.distance_to(p2), 111.20940183044317)

    def test_point_bearing(self):
        p1 = Point(1, 2)
        p2 = Point(1, 3)
        assert math.isclose(p1.bearing_to(p2), 89.9912735753)

    def test_point_next_point(self):
        p1 = Point(1, 2)
        p2 = p1.next_point(1, 0)
        assert p2 == Point(1.008983204953369, 2.0)

        # distance in km
        dist = p1.distance_to(p2)

        # haversine formula
        def haversine(lat1, lon1, lat2, lon2):
            R = 6372.8
            dLat = math.radians(lat2 - lat1)
            dLon = math.radians(lon2 - lon1)
            lat1 = math.radians(lat1)
            lat2 = math.radians(lat2)

            a = math.sin(dLat / 2)**2 + math.cos(lat1) * \
                math.cos(lat2) * math.sin(dLon / 2)**2
            c = 2 * math.asin(math.sqrt(a))
            return R * c

        assert math.isclose(dist, haversine(
            p1.y, p1.x, p2.y, p2.x), rel_tol=1e-3)

    def test_with_coords(self):
        p = Point(
            lat=-33.8670522,
            lon=151.1957362,
            timestamp=0,
            meta={'a': 1}
        )

        assert p.lat == -33.8670522
        assert p.lat == p.y
        assert p.lon == 151.1957362
        assert p.lon == p.x
        assert p.timestamp == 0
        assert p.meta == {'a': 1}
        assert p.xy == (151.1957362, -33.8670522)
