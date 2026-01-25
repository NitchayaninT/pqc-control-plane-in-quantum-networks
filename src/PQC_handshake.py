# Testing PQC integration with QuNetSim
# Insert a handshake step before allowing an entanglement request
from qunetsim.components import Host, Network
from qunetsim.objects import Message, Qubit, Logger
from qunetsim.backends import EQSNBackend
import time
import oqs
import os
import random

kem_name = "ML-KEM-768" # for kyber 768

network = Network.get_instance()
backend = EQSNBackend()

def pqc_handshake_establish(host, receiver_id, protocol, data_bytes):
# Alice -> Bob : "PQC_Hello"
# Alice runs encaps (pk), sends ciphertext to Bob
    print("PQC_SYN")
    host.send_classical(receiver_id, Message(protocol, data_bytes.hex()),await_ack=True) # block until ACK is received
    print("PQC_READY")

def pqc_handshake_ack(host, receiver_id):
# Bob runs Kyber Keygen -> sends public key to alice
# Bob runs decaps(ct) -> both now have shared secret K
    msg = host.get_classical(receiver_id, wait=10)
    if msg is None:
        return None
    if msg.content is None:
        return None
    else :
        print("PQC_ACK, msg=",msg)
        return msg

def pqc_keygen(host, receiver_id):
    kem_bob = oqs.KeyEncapsulation(kem_name)  
    pk = kem_bob.generate_keypair() # sets kem_bob.secret_key internally

    print("PQC_SEND_PK")
    host.send_classical(receiver_id, pk.hex()) # in qunetsim, they can only carry string msgs
    return kem_bob

def pqc_encaps(host, receiver_id):
    pk = host.get_classical(receiver_id, wait=10)
    if pk is None:
        raise RuntimeError(host.host_id+" did not receive PK")
    for m in pk:
        m = bytes.fromhex(m.content) # because we sent hex string
        with oqs.KeyEncapsulation(kem_name) as kem:
            ct, ss_enc = kem.encap_secret(m) # only accept a byte type object
        print("PQC_SEND_CT")
        host.send_classical(receiver_id,ct.hex())
    return ss_enc

def pqc_decaps(host, receiver_id, kem_host):
    ct = host.get_classical(receiver_id, wait=10)
    if ct is None:
        raise RuntimeError(host.host_id+" did not receive Ciphertext")
    for m in ct:
        m = bytes.fromhex(m.content)
        with oqs.KeyEncapsulation(kem_name) as kem:
            ss_dec = kem_host.decap_secret(m) # uses bob's internal private key to decap
            print("PQC_DONE")
    return ss_dec


def pqc_handshake(host1, host2):
    # 1) sends public key
    host2_kem = pqc_keygen(host2, host1.host_id) # gets host2's sk

    # 2) host1 encapsulates -> host2 gets ciphertext
    ss1 = pqc_encaps(host1, host2.host_id)

    # 3) host2 decapsulates -> get shared secret
    ss2 = pqc_decaps(host2, host1.host_id, host2_kem) # uses host2's kem object

    print("Alice SS:", ss1.hex())
    print("Bob   SS:", ss2.hex())
    print("MATCH:", ss1 == ss2)

    return ss1 # session key bytes

# ---------------- example setup ----------------
def main():
    nodes = ["Alice", "Bob"]
    network.start(nodes)

    # create host objects
    alice = Host("Alice")
    alice.add_connection("Bob")
    bob = Host("Bob")
    bob.add_connection("Alice")

    alice.start()
    bob.start()
    network.add_hosts([alice, bob])

# start session
    session_key = pqc_handshake(alice, bob)
    print("session key = ", session_key)

if __name__ == '__main__':
    main()