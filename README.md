# Message-Class-Aware Security for Multi-Hop Quantum Repeater Control Planes
Quantum repeater networks distribute entanglement across multiple hops, which enables applications such as long-distance quantum key distribution (QKD), distributed quantum computing, global quantum internet and networked sensing. 

They cannot function on quantum channels alone, each service depends on a classical control plane

## What does a control plane do?
- **Schedule entanglement attempts**
- **Report heralding outcomes** (after entanglement generation request attempts)
- **Sends Pauli correction** messages to rotate qubit
- **Carry bell-state measurement results** (measure local qubits in intermediate node and sends result to either if the repeater that its entangled with)
- **Coordinate entanglement swapping** at intermediate nodes 
- **Communicate node availability** and timeouts
## What do control plane messages contain?
- **Heralds** : Did this attempt succeed, on which link, in which time slot, which Bell state.
- **BSM outcomes** :  Which correction to apply (2 bits)
- **Scheduling and requests** : Who wants entanglement with whom, at what rate, at what fidelity
- **Session keys and handshake material** 
## Security Problems
1. Forge/Replay/==Delay control messages== can cause incorrect pauli corrections at the endpoints, trigger wasted entanglement attempts and desynchronize node schedules
	- **How can it happen?** : The packets got captured on a compromised machine or router
	- **What will happen after that?** : ==Wasted entanglement attempts,== desynchronized schedules
2. Adversary who records classical traffic today can attempt decryption later
	- **How can it happen?** : Compromised network device on the path, intercept traffic, the attacker records the key exchange over the network to agree on **symmetric key** so later, they can recover the session key and decrypt everything that key protected. They can also ==recover the private value from the public one to derive the shared secret and decrypt the session.==
    - **What will happen if they decrypt these messages? What can they learn from control  messages?** : **Traffic analysis,** if the application is QKD, ==the pattern of key requests reveals which organizations are exchanging keys and when== (that reveals the pattern of key establishment between them but not the keys ==themselves==). **Impersonation**, recovered long-term keys (signing key from the node's public key, which is in its certificate and freely available) let an attacker forge future messages or impersonate a node. Session key compromise is bounded to one session, ==signing key (CertificateVerify) compromise is ongoing and network-wide==, **Topology**, routing and calibration messages reveal the network graph
## Latency Problems
1. Some messages are **latency-critical and carry no secret**, others are **latency-tolerant and carry session state**
2. Security mechanism applied should follow from the **class of message** being protected
## Problem statements
- The control plane is unspecified from a security standpoint
	- There is ==no published classification of repeater control messages by the security guarantees they require==, and therefore no principled basis for choosing mechanisms
- Uniform security treatment is both wasteful and insufficient
	- Applying ==full confidentiality to every message imposes cost on latency-bound== that need only authenticity and freshness. 
- End-to-end-only protection is insufficient where intermediate repeaters must act on message contents
## Goal
To design and evaluate a security architecture for multi-hop quantum repeater control planes in which cryptographic mechanisms are assigned according to the security requirements and timing constraints of each class of control message
## System Architecture
- End Nodes: Request and receive end-to-end entanglement services.
- Repeater Nodes: Generate link-level entanglement, store quantum states, and perform entanglement swapping.
- Local Control-Plane Agents: Process PQC-secured control messages, verify authentication, check local resources, and instruct quantum operation controllers.
- PQC Security Module: Performs post-quantum key establishment and authentication for classical control-plane communication.
- Quantum Operation Controller: Simulates entanglement generation, entanglement swapping, memory timeout, and operation status.
- Log Agent: Collects local structured events from node components and forwards them to the centralized logging server.
- Centralized Security Logging Server: Receives, stores, and analyzes logs from all nodes for security and performance evaluation.

## Research Focus
This project focuses on the relationship between classical control-plane security and quantum-network operation outcomes. 
- Does PQC handshake overhead affect quantum operation timing?
- Can replay, delay, or packet drop behavior be detected from structured logs?
- Can authentication failures be linked to rejected control-plane messages?
- Can delayed classical control messages cause quantum memory timeout?

## Methodology
1. Threat Model
	- Output. Adversary capability table; per-message-type consequence-of-compromise analysis.
2. Message Taxonomy (Message types are extracted from published specifications)
3. Association topology analysis
	- End to end (source ↔ destination; repeaters forward opaque bytes)
	- Per hop (each adjacent pair)
	- Multi-unicast
	- Hybrid (per-hop for Class B, end-to-end for Class C)
	- Output : (network) Topology recommendation per message class    
4. Control plane architecture design
	- refining the author's prior design under the constraints derived in Phases 1–3.
	- Output :  
		- **The architecture** : layer decomposition, where security functions sit, key hierarchy, session state per node.
		- **The protocol specification** : Message sequence diagrams for single-hop and multi-hop, handshake mode, what's authenticated, what's encrypted, rekeying behaviour.
5. Implementation and evaluation
	- Cryptographic cost : real hardware
	- Protocol-level effects : simulated
## Internship period
This project is a ==continuation of my Internship Work.== During my internship period, I produced a prototype work which consists of control plane architecture, two handshake protocol designs and a preliminary overhead study. 
[Click here to see my internship work](/internship/README.md)

## Software Used : QuNetSim
Why QuNetSim?
QuNetSim is a high-level quantum network simulator designed for developing and testing quantum networking applications and protocols at the network and application layers. It enables rapid prototyping of control and communication protocols without requiring detailed physical-layer modeling. This makes QuNetSim well-suited for this project, which focuses on the design of a post-quantum secure classical control plane and its performance evaluation.
## How to run QuNetSim in your device?
1. Follow the instructions on the official website first
https://tqsd.github.io/QuNetSim/install.html

2. However, QuNetSim has not been updated to use newer versions of matplotlib, scapy and numpy. Make sure to downgrade them before installing QuNetSim
Recommended versions :
- matplotlib==3.5.3
- numpy==1.22.4
- scipy==1.9.3

Downgrade after installing a virtual environment
```bash
pip install matplotlib==3.5.3 numpy==1.22.4 scipy==1.9.3
```
3. Install QuNetSim
```bash
pip install QuNetSim
```
4. Once you log out and log back in, you have to reactivate a virtual environment and reinstall qunetsim
```bash
source .venv/bin/activate
pip install qunetsim
```
5. You can try running our python code to test it out
```bash
python3 ./src/PQC_handshake.py
```