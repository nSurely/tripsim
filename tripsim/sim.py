import osmnx as ox
import random
import networkx as nx
from geopy.distance import geodesic
from shapely.geometry import LineString
from typing import List, Tuple
import random
import osmnx as ox
from typing import List, Tuple, Optional

from .point import Point


def select_random_point(graph: nx.MultiDiGraph) -> Tuple[float, float]:
    """
    Selects a random point on the graph.

    Args:
        graph (nx.MultiDiGraph): the graph of the city/area where the trip takes place over the roads

    Returns:
        Tuple[float, float]: the coordinates of the point
    """
    coord = random.choice(list(graph.nodes()))
    # first get the lat and lon of the node
    return graph.nodes[coord]['x'], graph.nodes[coord]['y']


def simulate_straight_line(start_coord: Tuple[float, float],
                           end_coord: Tuple[float, float],
                           period_seconds: int = 5,
                           average_speed_mps: int = 10,
                           randomize_average_speed: bool = True) -> List[Point]:
    """
    Simulates driving in a straight line from a start point to a destination point,
    adding a point every period_seconds seconds at the average speed.

    Args:
        start_coord (Tuple[float, float]): the coordinates of the starting point
        end_coord (Tuple[float, float]): the coordinates of the destination point
        period_seconds (int, optional): the simulated time between points during the trip. Defaults to 5.
        average_speed_mps (int, optional): the average speed of the vehicle in meters per second. Defaults to 10.
        randomize_average_speed (bool, optional): whether to slightly randomize the average speed. Defaults to True.

    Returns:
        List[Point]: a list of points that represent the trip along the straight line
    """
    # Calculate the distance between the start and end points
    distance = geodesic(start_coord, end_coord).meters

    start_point = Point(lat=start_coord[0], lon=start_coord[1])
    start_point.add_meta('start', True)
    end_point = Point(lat=end_coord[0], lon=end_coord[1])
    end_point.add_meta('end', True)

    # Randomize the average speed
    if randomize_average_speed:
        average_speed_mps = random.uniform(
            average_speed_mps * 0.9,
            average_speed_mps * 1.1
        )

    # Calculate the time it takes to travel the distance at the average speed
    time = distance / average_speed_mps
    # Calculate the number of points to add
    num_points = int(time / period_seconds)

    if num_points == 0:
        return [start_point, end_point]

    # Calculate the distance between each point
    distance_between_points = distance / num_points

    # calculate the bearing between the start and end points
    # without using geodesic
    bearing = start_point.bearing_to(end_point)

    # Create a list of points
    points = []
    # Add the first point
    points.append(start_point)

    # Add the remaining points
    for i in range(1, num_points):
        # Calculate the distance along the line from the start point
        distance_from_start = distance_between_points * i

        # if the distance is greater than the distance between the start and end points
        # then just add the end point and break
        if distance_from_start > distance:
            points.append(end_point)
            break

        # Add the point to the list
        p = start_point.next_point(distance_from_start, bearing)
        p.add_meta('iterp', True)
        points.append(p)

    return points


def remove_duplicate_points(points: List[Point]) -> List[Point]:
    """
    Removes duplicate points from a list of points.

    Args:
        points (List[Point]): the list of points

    Returns:
        List[Point]: the list of points with duplicates removed
    """
    # Create a new list of points
    new_points = []
    # Add the first point
    new_points.append(points[0])
    # Add the remaining points
    for i in range(1, len(points)):
        # If the point is not the same as the previous point
        if points[i] != points[i - 1]:
            # Add the point to the list
            new_points.append(points[i])
    return new_points


def simulate_trip(graph: nx.MultiDiGraph,
                  start_time: float,
                  start_coord: Optional[tuple] = None,
                  end_coord: Optional[tuple] = None,
                  period_seconds: int = 5,
                  average_speed_mps: int = 10,
                  randomize_average_speed: bool = True) -> List[Point]:
    """
    Simulates a trip from a start point to a destination point.
    This function returns a list of points that represent the trip.

    Args:
        graph (nx.MultiDiGraph): the graph of the city/area where the trip takes place over the roads
        start_time (float): the time when the trip starts in seconds since the epoch
        start_coord (Optional[tuple], optional): the coordinates of the starting point. Defaults to None (will pick at random on the graph).
        end_coord (Optional[tuple], optional): the coordinates of the destination point. Defaults to None (will pick at random on the graph).
        period_seconds (int, optional): the simulated time between points during the trip. Defaults to 5.
        average_speed_mps (int, optional): the average speed of the vehicle in meters per second. Defaults to 10.
        randomize_average_speed (bool, optional): whether to slightly randomize the average speed. Defaults to True.

    Returns:
        List[Point]: _description_
    """
    start_coord = start_coord or select_random_point(graph)
    end_coord = end_coord or select_random_point(graph)

    # Get the distance between the start and end coordinates
    # distance = geodesic(start_coord, end_coord).meters

    # now we need to trace a line along the road network from the start to the end
    # we can do this by using the bearing to find the nearest node to the start coordinate
    # then we can find the nearest node to the end coordinate
    # then we can find the shortest path between the two nodes
    # then we can trace a line along the shortest path
    # then we can sample points along the line at a given distance interval
    # then we can add the points to the list of points

    # Get the node of the graph closest to the start coordinate
    start_node = ox.nearest_nodes(graph, start_coord[0], start_coord[1])
    # Get the node of the graph closest to the end coordinate
    end_node = ox.nearest_nodes(graph, end_coord[0], end_coord[1])

    # Get the shortest path between the start and end nodes
    path = nx.shortest_path(graph, start_node, end_node, weight='length')

    # Get the coordinates of the nodes in the path
    path_coords = [(graph.nodes[node]['x'], graph.nodes[node]['y'])
                   for node in path]

    # Create a line from the path coordinates
    line = LineString(path_coords)

    points = []

    last_time = start_time

    # simulate the trip along each segment of the line
    for i in range(len(line.coords) - 1):
        line_points = simulate_straight_line(
            line.coords[i],
            line.coords[i + 1],
            period_seconds,
            average_speed_mps,
            randomize_average_speed
        )

        # add time to each point
        # then propagate the time to the next point
        for point in line_points:
            point.set_timestamp(last_time)
            last_time += period_seconds

        points.extend(line_points)

    return remove_duplicate_points(points)
