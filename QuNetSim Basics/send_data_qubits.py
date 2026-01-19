# Send a data qubit from Alice to Dean, who sits 2 hops away from Alice in the network
from qunetsim.components import Host, Network
from qunetsim.objects import Message, Qubit, Logger
from qunetsim.backends import EQSNBackend

Logger.DISABLED = True

# create the EQSN backend object
backend = EQSNBackend()

# Sender protocol
def protocol_sender(sender, receiver): # parameters = sender (host obj), receiver (host id, str)
    # Alice sends 10 qubits to Dean after applying an X gate on the qubit
    for i in range(10):
        # Create a qubit object, parameter is Host id
        q = Qubit(sender)
        q.X() # Bit flip
        q_id, _ = sender.send_qubit(receiver, q, await_ack=True) # wait for ACK from Dean
        # send_qubit returns 2 values, the q_id that was sent and a boolean value that says if the ACK arrived or not
def protocol_receiver(receiver, sender):
    for i in range(10):
        q_rec = receiver.get_qubit(sender, wait=10)
        if q_rec is not None:
            m = q_rec.measure()
            print("Results of the measurements for q_id are ", str(m))
        else:
            print("Qubit did not arrive")

# Configuring a network
def main():
    network = Network.get_instance()
    nodes = ["Alice", "Bob", "Eve", "Dean"] # host ids
    network.start(nodes)

    # Create host objects
    host_alice = Host("Alice")
    host_alice.add_connection("Bob")
    host_alice.start()

    host_bob = Host("Bob")
    host_bob.add_connection("Alice")
    host_bob.add_connection("Eve")
    host_bob.start()

    host_eve = Host("Eve")
    host_eve.add_connection("Bob")
    host_eve.add_connection("Dean")
    host_eve.start()

    host_dean = Host("Dean")
    host_dean.add_connection("Eve")
    host_dean.start()

    # Add Host Objects to the network
    network.add_host(host_alice)
    network.add_host(host_bob)
    network.add_host(host_eve)
    network.add_host(host_dean)

    # How the network looks like : 
    # Alice -- Bob -- Eve -- Dean

    t1 = host_alice.run_protocol(protocol_sender, (host_dean.host_id,)) # pass reciever id, not the obj
    t2 = host_dean.run_protocol(protocol_receiver, (host_alice.host_id,), blocking = True) # pass sender id, not the obj

    network.draw_classical_network()
    network.stop(stop_hosts=True)

if __name__ == '__main__':
    main()