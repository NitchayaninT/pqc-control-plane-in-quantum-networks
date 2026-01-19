"""Generate a network with 4 nodes, then send an EPR pair from one end 
of the link to the other
Classical info is routed through Host B
Quantum info is routed through Host C
"""
from qunetsim.components import Host, Network
from qunetsim.objects import Message, Qubit, Logger
from qunetsim.backends import EQSNBackend
import time

Logger.DISABLED = True

# create the EQSN backend object
backend = EQSNBackend()

def protocol_sender(sender, receiver):
    """
    Sender protocol for sending 5 EPR pairs.

    Args:
        host (Host): The sender Host.
        receiver (str): The ID of the receiver of the EPR pairs.
    """
    for i in range(5):
        print('Sending EPR Pair %d' % (i+1))
        epr_id, ack_arrived = sender.send_epr(receiver, await_ack=True)
        # Returns:(str, bool): If await_ack=True, return the ID of the EPR pair and the status of the ACK
        if ack_arrived:
             # Receiver got the EPR pair and ACK came back
             # safe to use the EPR pair.
            q = sender.get_epr(receiver, q_id=epr_id)
            # Gets the EPR that is entangled with another host in the network.
            # get epr pair from the receiver (id) with q_id = epr_id
            # returns qubit object
            print('Host 1 measured : %d' % q.measure())
        else:
            print('The EPR pair was not properly established')
        print('Sender protocol done')

def protocol_receiver(receiver, sender):
    """
    Receiver protocol for receiving 5 EPR pairs.

    Args:
        host (Host): The sender Host.
        sender (str): The ID of the sender of the EPR pairs.
    """
    for i in range(5):
        q = receiver.get_epr(sender, wait=5)
        # q is None if the wait time expired
        if q is not None:
            print('Host 2 measured: %d' % q.measure())
        else:
            print('Host 2 did not receive an EPR pair')
    print('Receiver protocol done')

def main():
    network = Network.get_instance()
    nodes = ['A','B','C']
    network.start(nodes)

    # create host objects
    host_A = Host('A',backend)
    host_A.add_connection('B')
    host_A.start()

    host_B = Host('B',backend)
    host_B.add_connection('A')
    host_B.add_connection('C')
    host_B.start()

    host_C = Host('C',backend)
    host_C.add_connection('B')
    host_C.start()

    network.add_host(host_A)
    network.add_host(host_B)
    network.add_host(host_C)

    t1 = host_A.run_protocol(protocol_sender,(host_C.host_id,))
    t2 = host_C.run_protocol(protocol_receiver,(host_A.host_id,), blocking=True)
    
    
    time.sleep(0.2) #delay so that the sender is able to receive the ACK before network stops simulating
    network.stop(stop_hosts=True)

if __name__ == '__main__':
    main()