# Entanglement simple example
# How to add a custom routing function that considers the entanglement in network
''' Network Configuration : 
- A <==> node_1; A <==> node_2
- B <==> node_2; B <==> node_2
'''
from qunetsim.components import Host, Network
from qunetsim.objects import Message, Qubit, Logger
from qunetsim.backends import EQSNBackend
import time
import networkx

def generate_entanglement(host):
    # Generate entanglement if the host has nothing to process (i.e. is idle)
    while True:
        if host.is_idle():
            host_connections = host.get_connections() # get list of connections for this host
            for connection in host_connections:
                if connection['type'] == 'quantum':
                    num_epr_pairs = len(host.get_epr_pairs(connection['connection'])) # get number of epr pairs established with current host
                    if num_epr_pairs < 4:
                        # send epr pair to the receiver(s) that are connected to the current host
                        # ONLY if the current host has only established less than 4 epr pairs with the nodes that are connected to it
                        host.send_epr(connection['connection'], await_ack=True) 
        time.sleep(5)

def routing_algorithm(di_graph, source, dest):
    """
    Entanglement based routing function. Note: any custom routing function must
    have exactly these three parameters and must return a list ordered by the steps
    in the route.

    Args:
        di_graph (networkx DiGraph): The directed graph representation of the network.
        source (str): The sender ID
        target (str: The receiver ID
    Returns:
        (list): The route ordered by the steps in the route.
    """

    # Build a graph with the vertices, hosts, edges, connections
    entanglement_network = networkx.DiGraph()
    nodes = di_graph.nodes() # nodes within the graph representation
    # Generate entanglement network
    for node in nodes:
        host = network.get_host(node)
        host_connections = host.get_connections()
        for connection in host_connections:
            if connection['type'] == 'quantum':
                num_epr_pairs = len(host.get_epr_pairs(connection['connection']))
                if num_epr_pairs == 0:
                    # when there is no entanglement, add a large weight to that edge
                    entanglement_network.add_edge(host.host_id, connection['connection'], weight=1000)
                else :
                    # the weight of each edge is the inverse of the amount of entanglement shared on that link
                    entanglement_network.add_edge(host.host_id, connection['connection'], weight=1. / num_epr_pairs)

    try:
        # Compute the shortest path on this newly generated graph
        # from sender to receiver and return the route
        route = networkx.shortest_path(entanglement_network, source, dest, weight='weight')
        print('-------' + str(route) + '-------')
        return route
    except Exception as e:
        Logger.get_instance().error(e)

def main():
    network = Network.get_instance()
    nodes = ['A', 'node_1', 'node_2', 'B']
    network.use_hop_by_hop = False # recalculate the route just once from the beginning
    network.set_delay = 0.1
    network.start(nodes)

    A = Host('A')
    A.add_connection('node_1')
    A.add_connection('node_2')
    A.start()

    node_1 = Host('node_1')
    node_1.add_connection('A')
    node_1.add_connection('B')
    node_1.start()

    node_2 = Host('node_2')
    node_2.add_connection('A')
    node_2.add_connection('B')
    node_2.start()

    B = Host('B')
    B.add_connection('node_1')
    B.add_connection('node_2')
    B.start()

