# Testing PQC integration with QuNetSim
# Insert a handshake step before allowing an entanglement request
from qunetsim.components import Host, Network
from qunetsim.objects import Message, Qubit, Logger
from qunetsim.backends import EQSNBackend
from time import perf_counter_ns
import time
import networkx
import oqs
import random

network = Network.get_instance()
backend = EQSNBackend()

def establish_PQC_handshake(host, target):
# Alice -> Bob : "PQC_Hello"
# Alice runs encaps (pk), sends ciphertext to Bob
    while True:
        if host.is_idle():
            q = Qubit(host)
            q_id,_ = host.send_qubit(target, q, await_ack=True)
            print("PQC_Hello")


def receive_PQC_handshake(host, target):
# Bob runs Kyber Keygen -> sends public key to alice
# Bob runs decaps(ct) -> both now have shared secret K
    q_rec = host.get_qubit(target, wait=10)
    if q_rec is not None:
        m = q_rec.measure()
        print("PQC_ACK")

#def establish_entanglement(host, target):
# Alices sends ENT_REQUEST for the first request

#def receive_entanglement(host, target):
# Bob verifies (ACK) then proceed to establish EPR pair