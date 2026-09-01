# Internship Work
- [Control plane architecture design](internship/Control%20Plane%20Design/README.md)
- [Understand a Quantum Network simulation tool called "QuNetSim" and write simple codes](#qunetstim)
- Literature Review about NV-repeater nodes and its operations
- Understand quantum network services
	- Entanglement Generation
	- Entanglement Swapping
- Design a secure control plane architecture
	- with PQC (security module)
- Design PQC handshake protocols for Single-Hop and Multi-Hop
- Research question **" How much does PQC cost?"**
## QuNetSim
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