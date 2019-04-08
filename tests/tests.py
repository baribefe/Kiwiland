from graphs.graphs import railroadGraph
import unittest

class railroadGraphTest(unittest.TestCase):

    def initialize_graph(self):
        self.rail_network = railroadGraph()

    def build_test_graph(self):

        # Add nodes to graph

        self.rail_network.add_town_to_graph('A')
        self.rail_network.add_town_to_graph('B')
        self.rail_network.add_town_to_graph('C')
        self.rail_network.add_town_to_graph('D')
        self.rail_network.add_town_to_graph('E')

        # Add connecting edges 

        self.rail_network.add_route_to_graph('A', 'B', 5)
        self.rail_network.add_route_to_graph('B', 'C', 4)
        self.rail_network.add_route_to_graph('C', 'D', 8)
        self.rail_network.add_route_to_graph('D', 'C', 8)
        self.rail_network.add_route_to_graph('D', 'E', 6)
        self.rail_network.add_route_to_graph('A', 'D', 5)
        self.rail_network.add_route_to_graph('C', 'E', 2)
        self.rail_network.add_route_to_graph('E', 'B', 3)
        self.rail_network.add_route_to_graph('A', 'E', 7)

    # Carry out all test calculations

    def run_test1(self):
        d_abc   = self.rail_network.get_distance_between_towns('A', ['B','C'])
        self.assertEqual(d_abc, 9)

    def run_test2(self):
        d_ad    = self.rail_network.get_distance_between_towns('A', 'D')
        self.assertEqual(d_ad,5)

    def run_test3(self):
        d_adc   = self.rail_network.get_distance_between_towns('A', ['D','C'])
        self.assertEqual(d_adc,13)

    def run_test4(self):
        d_aebcd = self.rail_network.get_distance_between_towns('A', ['E','B','C','D'])
        self.assertEqual(d_aebcd,22)

    def run_test5(self):
        d_aed   = self.rail_network.get_distance_between_towns('A', ['E','D'])
        self.assertEqual(d_aed, 'NO SUCH ROUTE')

    def run_test6(self):
        all_C_C_max3_trips = self.rail_network.trips_starting_at_town_with_number_of_stops('C', 'C', number_of_stops=3, trip_type = 'max')
        self.assertEqual(all_C_C_max3_trips, 2)

    def run_test7(self):
        all_A_C_exactly4_trips = self.rail_network.trips_starting_at_town_with_number_of_stops('A', 'C', number_of_stops=4, trip_type = '')
        self.assertEqual(all_A_C_exactly4_trips, 3)

    def run_test8(self):
        shortest_from_A_to_all_nodes = self.rail_network.dijkstra_all_shortest_paths_from_origin('A')
        self.assertEqual(shortest_from_A_to_all_nodes, 9)

    def run_test9(self):
        shortest_from_B_to_all_nodes = self.rail_network.dijkstra_all_shortest_paths_from_origin('B')
        self.assertEqual(shortest_from_B_to_all_nodes, 9)

    def run_test101(self):
        distance_C_C_max_dist_30 = self.rail_network.routes_with_maximum_distance('C', 'C', 30)
        self.assertEqual(distance_C_C_max_dist_30, 7)

