from tripsim import simulate_trip
import osmnx as ox


class TestFullSim:
    def test_simulate_trip(self):
        graph = ox.graph_from_place('Douglas, Ireland', network_type='drive')
        trip = simulate_trip(graph)
        assert trip is not None
        assert len(trip) > 0
