# Design and Evaluation of a PQC-Secured Quantum Repeater Control Plane with Centralized Security Logging
This project focuses on the design and evaluation of a post-quantum secure classical control plane for quantum repeater networks. The project investigates how Post-Quantum Cryptography (PQC) can be applied to protect classical control-plane communication used to coordinate quantum network operations such as entanglement generation and entanglement swapping.

The system also introduces a centralized security logging component to collect structured events from simulated end nodes, repeater nodes, local control-plane agents, PQC security modules, and quantum operation controllers. These logs are used to analyze abnormal behavior under normal and attack scenarios, including replay attempts, MAC/signature verification failures, delayed control messages, suspected packet drops, memory timeout, and entanglement operation failures.

## Problem
Quantum repeater networks rely on classical control messages to coordinate quantum operations across multiple nodes. These messages may include entanglement generation requests, entanglement swapping requests, measurement results, status reports, and resource availability updates. If the classical control channel is not protected against future quantum-capable adversaries, sensitive control-plane information may be exposed or manipulated.

This project explores a PQC-secured control-plane workflow where nodes establish post-quantum secure classical sessions before executing quantum network operations. A centralized logging system is added to provide security visibility and support analysis of how classical control-plane events affect quantum operation outcomes.

## Goal
Design a secure classical control plane that 
- Uses PQC (KyberKEM) for handshake establishment process in classical channel
- Coordinates entanglement generation & swapping
- Preserves coherence of NV nuclear memories
- Resists Store now, decrypt later and MITM attacks
- Evaluate trade off between security overhead & quantum performance

## System Architecture
- End Nodes: Request and receive end-to-end entanglement services.
- Repeater Nodes: Generate link-level entanglement, store quantum states, and perform entanglement swapping.
- Local Control-Plane Agents: Process PQC-secured control messages, verify authentication, check local resources, and instruct quantum operation controllers.
- PQC Security Module: Performs post-quantum key establishment and authentication for classical control-plane communication.
- Quantum Operation Controller: Simulates entanglement generation, entanglement swapping, memory timeout, and operation status.
- Log Agent: Collects local structured events from node components and forwards them to the centralized logging server.
- Centralized Security Logging Server: Receives, stores, and analyzes logs from all nodes for security and performance evaluation.

## Research Focus
This project focuses on the relationship between classical control-plane security and quantum-network operation outcomes. The logging system is designed to help answer questions such as:

- Does PQC handshake overhead affect quantum operation timing?
- Can replay, delay, or packet drop behavior be detected from structured logs?
- Can authentication failures be linked to rejected control-plane messages?
- Can delayed classical control messages cause quantum memory timeout?
- Can centralized logs explain why entanglement generation or swapping failed?

## Methodology
- [PQC Control plane architecture design](./Control%20Plane%20Design/README.md)
	- Layered control-plane stack
	- Deterministic scheduling policies
	- Local Control plane Agent design for each node
- Quantum Repeater Network Model 
	- Network Topology
- Threat Model
- Quantum Operation Simulation
- Security Log Design
- Log Agent Implementation
- Centralized Security Logging Server
- Attack and Abnormal Scenario Simulation
- Rule-based security Analysis
- Evaluation (Is using PQC to secure classical information worth it?)
	- PQC computational latency compared with non-PQC latency
	- Network transmission overhead using huge PQC elements and not using it
	- Impact of security overhead in entanglement generation and entanglement swapping
	- Eavesdropping test between using PQC and non-PQC

## Tools and Technologies (PLANNING)
- Python
- QuNetSim or Sequence
- liboqs / Open Quantum Safe for PQC algorithms
- ML-KEM for post-quantum key establishment
- ML-DSA for post-quantum signatures
- HMAC for message authentication verification
- FastAPI for centralized logging server
- JSON / JSONL structured logs
- SQLite or file-based storage for log analysis

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