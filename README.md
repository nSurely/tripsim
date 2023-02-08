# tripsim  

Driving trip simulator for building a series of coordinates that can be used for testing telematics systems.

> :warning: This is quite a simplified implementation that should not be used for anything beyond simple load testing or distance calculations.  

## Getting Started  

> Currenlty, only python versions 3.9+ are supported.  

```cmd
pip install tripsim
```

## Simulating a Trip  

Here we will simulate driving and plotting the points taken from one random point to another in a city.  

```python
from tripsim import simulate_trip

# other imports for this example
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import osmnx as ox


def main():
    # Get the graph of the city of Cork
    graph = ox.graph_from_place('Cork City, Ireland', network_type='drive')

    # the simulated trip will return a list of points
    # each point has a latitude and longitude, along with a timestamp (in seconds)
    trip = simulate_trip(graph)

    # adjust your styling accordingly
    _, ax = ox.plot_graph(
        graph, dpi=180,
        node_color='green',
        node_size=1,
        node_alpha=0.1,
        node_edgecolor='white',
        node_zorder=5,
        edge_color='white',
        edge_linewidth=2,
        edge_alpha=0.1,
        show=False,
        close=False
    )

    # the points are a dataclass with a few convenience methods
    coords = [
        (point.get_lat(), point.get_lon())
        for point in trip
    ]

    # here we are setting the list of coords as a LineString
    # for easy plotting
    coords_graph_line = LineString(coords)
    x, y = coords_graph_line.xy

    ax.plot(x, y, '-o', color='red',
            markersize=3, alpha=0.7, zorder=1)

    plt.show()


if __name__ == '__main__':
    main()

```

The created trip should look something like this when plotted.  

![trip](https://i.ibb.co/zZBZhJx/cork-trip.png)  


## Handling Points  

A trip is just a list of `Point` instances, which represent a point on the earth's surface. The `Point` dataclass gives you a few convenience methods.  

```python
from tripsim import Point

import time

# create a point
point = Point(
    lat=-33.8670522,
    lon=151.1957362
)

# x = longitude
# y = latitude
assert point.lat == -33.8670522
assert point.lat == point.y
assert point.lon == 151.1957362
assert point.lon == point.x
assert point.xy == (151.1957362, -33.8670522)

# you can add timestamps to Points to replicate
# collecting GPS data on an interval
point.set_timestamp(time.time())

# you can create new Points relative to this one

# new point 1km north
point_2 = point.next_point(
    distance=1,
    bearing=0
)

# inequality works on points lat/lon
assert point != point_2

assert point.distance_to(point_2) == 1.0
assert point.bearing_to(point_2) == 0.0
```
