from collections import defaultdict
import pprint

class railroadGraph(object):

    def __init__(self, town_dict=None, route_dict=None):

        # town_dict: dictionary with keys representing origin towns and the values
        # containing a list of lists of destination towns 
        # e.g. {'Kaitaia': [Invercargill, 'SomeOtherTown']}

        # route_dict: dictionary with keys as tuple representing routes between towns 
        # and the values are the distances between them e.g. {(Kaitaia,Invercargill) = 10}

        # Initialise with an empty graph dictionary if an initial graph
        # is not provided

        if town_dict == None:
            self.town_dict = {}
        else:
            self.town_dict = town_dict

        # Initialise an empty dictionary of routes if a route dictionary 
        # is not provided

        if route_dict == None:
            self.route_dict = {}
        else:
            self.route_dict = route_dict

    # Add a new town to the railroad graph
    def add_town_to_graph(self, town_name):

        # Add a new town to the railroad graph if not already present
        if town_name not in self.town_dict.keys():
            self.town_dict[town_name] = []

    def add_connection_to_town(self, town_name, connectioning_town_name):

        # Add a new connection to a town in the railroad graph
        if town_name not in self.town_dict.keys():
            self.town_dict[town_name] = [connectioning_town_name]
        else:
            self.town_dict[town_name].append(connectioning_town_name)

    def add_route_to_graph(self, origin_town, destination_town, distance):
        
        # Add destination_town to the connections from origin_town

        if origin_town in self.town_dict.keys():
            self.town_dict[origin_town].append(destination_town)
        else:
            self.town_dict[origin_town] = [destination_town]
        
        # Next, add the connection to self.route_dict

        if (origin_town, destination_town) not in self.route_dict.keys():
            self.route_dict[(origin_town, destination_town)] = distance

    def get_distance_between_towns(self, origin_town, destination_towns):

        # First check if origin town is in the graph

        if origin_town not in self.town_dict.keys():
            print("The origin town: ", origin_town, ", does not exist in railroad graph")
        else:

            # Check if there is a connection between origin town and
            # destination town. Look for ways to optimize this

            #destination_towns can either be a single string or a list of strings for a
            #multiple town iternary.

            if not isinstance(destination_towns, (list, tuple)):
                destination_towns = [destination_towns]

            total_distances = 0
            no_such_route = False

            for i in range(len(destination_towns)):

                # First deal with the case of only one destination town
                if i == 0:
                    connections_from_origin = self.town_dict[origin_town]
                    destination_town = destination_towns[0]

                    # Recursively add the distances for each connection from origin
                    if destination_town in connections_from_origin:
                        if (origin_town,destination_town) in self.route_dict.keys():
                            total_distances = total_distances + self.route_dict[(origin_town,destination_town)]
                    else:
                        no_such_route = True
                        break

                # Then consider a multi-town input

                elif i > 0: 
                    new_origin_town = destination_towns[i-1]
                    new_destination_town = destination_towns[i]
                    new_connections_from_origin = self.town_dict[new_origin_town]

                    # Recursively add the distances for each connection from origin
                    if  new_destination_town in new_connections_from_origin:
                        if (new_origin_town,new_destination_town) in self.route_dict.keys():
                            total_distances = total_distances + self.route_dict[(new_origin_town,new_destination_town)]
                    else:
                        no_such_route = True
                        break

        if no_such_route:
            return "NO SUCH ROUTE"
        else:
            return total_distances
    
    def trips_starting_at_town_with_number_of_stops(self, origin_town, destination_town, number_of_stops, trip_type = '', routes = []):

        trips = 0
        routes.append(origin_town)
        
        # Verify that origin and destination exist

        if (origin_town in self.town_dict.keys() ) and (destination_town in self.town_dict.keys()):

            # Stop if no more stops can be made

            if number_of_stops == 0:
                return 0

            # Recursively add the trips for each connection from origin town. If we are at the destination
            # and the remaining number of allowed stops is 1 or we have a hard maximum number of stops we
            # can do, we increment trip number.

            for new_origin in self.town_dict[origin_town]: 
                if new_origin == destination_town and (trip_type == 'max' or number_of_stops == 1):
                    trips = trips + 1
                    routes.append(new_origin)
                routes.append(new_origin)
                trips += self.trips_starting_at_town_with_number_of_stops(new_origin, destination_town, number_of_stops-1, trip_type)
        else:
            print('NO SUCH ROUTE')

        return trips

    def dijkstra_all_shortest_paths_from_origin(self, origin_town):

        # Implementation of the Dijksta algorith to find the shortest path from an origin town
        # to all other accessibly towns (nodes) in the graph.

        # Set the distance from the origin town to be zero.
        
        completed_towns = {}
        visited_towns = {origin_town: 0}

        while visited_towns:
            town_with_min_dist = min(visited_towns, key=visited_towns.get)
            cost_to_min_town = visited_towns.pop(town_with_min_dist)

            # Get all connections and the distances (to them) from the town with the minimum distance
            # among the visited towns

            connections = self.town_dict[town_with_min_dist]
            travel_distances = []
            for connection in connections:
                if (town_with_min_dist, connection) in self.route_dict.keys():
                    travel_distances.append( (connection, self.route_dict[(town_with_min_dist, connection)]) )

            
            for route_distance in travel_distances:
                r, d = route_distance
                if r not in completed_towns:
                    comparison_min = cost_to_min_town + d
                    if r not in visited_towns:
                        visited_towns[r] = comparison_min
                    else:
                        visited_towns[r] = min(comparison_min, visited_towns[r])

            # For some routes (eg C to C) it is required to not designate
            # a route as completed if the travel distance is not greater
            # than zero.

            if town_with_min_dist != origin_town or cost_to_min_town > 0:
                completed_towns[town_with_min_dist] = cost_to_min_town
        return completed_towns

    def routes_with_maximum_distance(self, origin_town, destination_town, maximum_distance):

        total_dist = 0

        # Get all connections and distances from origin_town

        connections = self.town_dict[origin_town]
        travel_distances = []
        for connection in connections:
            if (origin_town, connection) in self.route_dict.keys():
                travel_distances.append( (connection, self.route_dict[(origin_town, connection)]) )

        # For every connection from this origin, recursively get distances for every connection until 
        # destination_town within maximum distance limits

        for route_distance in travel_distances:
            new_town, distance_to_new_town = route_distance
            if new_town == destination_town and distance_to_new_town < maximum_distance:
                total_dist  = total_dist + 1
            if distance_to_new_town < maximum_distance:
                total_dist  = total_dist + self.routes_with_maximum_distance(new_town, destination_town, maximum_distance-distance_to_new_town)

        return total_dist

# Create graph and run all tests. These tests can also be done by going up one directory and running [python -m unittest]

if __name__ in '__main__':

    rail_network = railroadGraph()
    rail_network.add_town_to_graph('A')
    rail_network.add_town_to_graph('B')
    rail_network.add_town_to_graph('C')
    rail_network.add_town_to_graph('D')
    rail_network.add_town_to_graph('E')

    rail_network.add_route_to_graph('A', 'B', 5)
    rail_network.add_route_to_graph('B', 'C', 4)
    rail_network.add_route_to_graph('C', 'D', 8)
    rail_network.add_route_to_graph('D', 'C', 8)
    rail_network.add_route_to_graph('D', 'E', 6)
    rail_network.add_route_to_graph('A', 'D', 5)
    rail_network.add_route_to_graph('C', 'E', 2)
    rail_network.add_route_to_graph('E', 'B', 3)
    rail_network.add_route_to_graph('A', 'E', 7)

    # Print graph (meaningful for a graph of this size)

    print('Dictionary data structure used to represent the town network: ')
    pprint.pprint(rail_network.town_dict)

    print('Edges (routes) representing distances between towns: ')
    pprint.pprint(rail_network.route_dict)

    print('Running Tests 1 to 10')

    d_abc   = rail_network.get_distance_between_towns('A', ['B','C'])
    d_ad    = rail_network.get_distance_between_towns('A', 'D')
    d_adc   = rail_network.get_distance_between_towns('A', ['D','C'])
    d_aebcd = rail_network.get_distance_between_towns('A', ['E','B','C','D'])
    d_aed   = rail_network.get_distance_between_towns('A', ['E','D'])
    all_C_C_max3_trips = rail_network.trips_starting_at_town_with_number_of_stops('C', 'C', number_of_stops=3, trip_type = 'max')
    all_A_C_exactly4_trips = rail_network.trips_starting_at_town_with_number_of_stops('A', 'C', number_of_stops=4, trip_type = '')
    shortest_from_A_to_all_nodes = rail_network.dijkstra_all_shortest_paths_from_origin('A')
    shortest_from_B_to_all_nodes = rail_network.dijkstra_all_shortest_paths_from_origin('B')
    distance_C_C_max_dist_30 = rail_network.routes_with_maximum_distance('C', 'C', 30)

    print('Test 1: ', d_abc)
    print('Test 2: ', d_ad)
    print('Test 3: ', d_adc)
    print('Test 4: ', d_aebcd)
    print('Test 5: ', d_aed)
    print('Test 6: ', all_C_C_max3_trips)
    print('Test 7: ', all_A_C_exactly4_trips)
    print('Test 8: ', shortest_from_A_to_all_nodes['C'])
    print('Test 9: ', shortest_from_B_to_all_nodes['B'])
    print('Test 10: ', distance_C_C_max_dist_30)

