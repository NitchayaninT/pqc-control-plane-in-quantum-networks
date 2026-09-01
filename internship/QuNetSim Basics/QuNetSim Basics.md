# QuNetSim Basics
- Network Components
	- [Host](#host)
	- [Network](#network)
	- [Protocols](#protocols)
- Network Objects
	- [Message](#message)
	- [Qubit](#qubit)
	- [Quantum Storage](#quantum-storage)
	- [Classical Storage](#classical-storage)
	- [Quantum Connection](#quantum-connection)
	- [Classical Connection](#classical-connection)
	- [Packet](#packet)
	- [Routing Packet](#routing_packet)
- Backends

## Network Components
### Host
---
- Equivalent to Node
- Represents application layer
- Roles : 
	- **Run applications** (a protocol)
	- **Relay packets** in the network (forwarded)
	- **Sniff Packets,** Eavesdrop on channels to manipulate payload of the packet
		- By applying random noise to any qubit or change the classical messages that are routed through them
- Programmed with a set of features that can be used to write network applications
- Up to protocol developer to ==configure how the nodes behave==
- In most cases, once the network is established, users will run specific protocols on the nodes 
#### Methods 
- `add_connection(host_id)` : Add a classical and quantum connection to the host with host_id

- `get_classical(host_id, wait=N)` : Get a classical message from sender with host_id and wait N seconds for it

- `get_qubit (host_id, wait=N)` : Get a data qubit from sender with host_id and wait N seconds for it

- `get_qubits (host_id)` : Get all data qubits from sender with host_id

- `get_epr (host_id, q_id=q_id)` : Get EPR pair with qubit ID = q_id from sender with host_id. If q_id = None, then get the first free EPR pair

- `get_epr_pairs (host_id)` : Get all EPR pairs established with host with host_id

- `send_classical (host_id, message, await_ack=<bool>)` : Send the classical message to host with host_id. Block until ACK arrives if await_ack = True

- `send_key (host_id, key_size)` : Send a secret key via QKD of length key_size to host with ID receiver_id

- `send_qubit (host_id, qubit, await_ack=<bool>)` : Send qubit to host with host_id. Block until ACK arrives if await_ack = True

- `send_superdense (host_id, message, await_ack=<bool>)` : Send a message (one of '00', '01', '10' or '11') as a superdense message

- `send_teleport(host_id, qubit, await_ack=<bool>)` : Teleport qubit to host with host_id

- `send_epr(host_id, qubit_id=<None>, await_ack=<bool>)` : Created a shared EPR pair with the host with host_id. qubit_id = None means QuNetSim will auto-assign the ID

- `send_ghz([host_id_list], qubit_id=<None>, await_ack=<bool>)` : Creates a shared GHZ state with all hosts in the list [host_id_list]

- `shares_epr(host_id)` : Returns if the host shares entanglement already with host with host_id (just checks its storage)

- `run_protocol(protocol, protocol_params)` : Run the function protocol with the parameters protocol_params

#### What is an EPR Pair?
An EPR pair is two entangled qubits shared between two nodes (hosts)
Once created, the qubits are correlated no matter the distance (link)
- **shares_EPR** : Do we currently have any EPR pairs stored with host_id?
	- Is entanglement already available with that host?
- **send_EPR** : Create and distribute an EPR pair between **us and host_id**
	- Initiates entanglement generation with the remote host
	- **If successful**, both hosts end up storing one qubit that forms the EPR pair
- **get_EPR** : Give us one EPR qubit from my storage that is **entangled with host_id**
	- if q_id is provided : fetch that specific EPR qubit (by ID)
	- if q_id = None : fetch the first available/free EPR qubit with that host
	- What we get : a qubit object (our half of the EPR pair, while the host_id has the other half in their storage)
When 2 nodes share an EPR pair : 
- Node A has qubit A
- Node B has qubit B
- There 2 qubits form **one joint quantum state** even if they are far apart, they behave like one system, not 2 independent qubits
- It creates correlated outcomes (via measurement at the node), not messages
#### What entanglement enables
- **Quantum Teleportation**
- **Quantum Key Distribution (QKD)**
- **Secure Control & Authentication** : Device authentication via correlation tests, trust establishment before quantum operations
- **Entanglement Swapping** : A - B share entanglement, B - C share entanglement. Then B can perform a joint measurement and suddenly, A - C become entangled without ever interacting

**However,** in my project, the goal is to **secure a classical control plane**, where I use PQC to **protect the "Classical Messages"** like : "Create EPR between A and B", "ACK recieved", "Retry entanglement" from future quantum attacks. But quantum channel can still be noisy due to qubits being fragile when transmitting over quantum network when doing **entanglement establishment**. That's handled by Quantum error correction (QEC) + purification instead of PQC, which is not the main focus in this project.

**Summary** : Entanglement links two distant qubits into a single quantum system, enabling secure key generation, state transfer, and scalable quantum networking capabilities that cannot be achieved with classical communication alone
#### Host Object
`_class_ qunetsim.components.host.Host(_host_id_, _backend=None_)`
- Host object acting as either a **router node** or an **application host node**

More info about the object's methods : https://tqsd.github.io/QuNetSim/components/host.html

`qunetsim.components.host._get_qubit(_store_, _host_id_, _q_id_, _purpose_, _wait=0_)`
- **Gets the data qubit** received from another host in the network. 
	- **store** – The qubit storage to retrieve the qubit
	- **host_id** (_str_) – The ID of the host that data qubit to be returned is received from.
	- **q_id** (_str_) – The qubit ID of the data qubit to get.
	- **purpose** (_str_) – The intended use of the qubit
### Network
---
In each simulation, one must configure a network with hosts. Each host defines its classical and quantum connections and when the host is added to the network, the network builds on the **two graph objects for each type of connection it maintains.** 

One can define their own routing algorithms for each type of network. Default = Shortest path route between the 2 hosts

#### Methods
- `add_host(host)` : add a host to the network

- `remove_host(host)` : remove a host from the network

- `update_host(host)` : Updates the network graph when the connections of a host change

- `get_host(host_id)` : Get the host object given the host_id

- `get_APR()` : Get the information for all the hosts in the network

- `(property) quantum_routing_algo(function)` : Property for the quantum routing algorithm. It should be a function with parameters that take a **source ID and a destination ID** and **returns an ordered list** which represents the route

- `(property) classical_routing_algo(function)` : Property for the classical routing algorithm. It should be a function with parameters that take a source ID and a destination ID and returns an ordered list which represents the route

- `(property) use_hop_by_hop(bool)` : If the network should recalculate the route at each node in the route (set to True) or just once at the beginning (set to False)

- `(property) delay(float)` : the amount of delay the network should have. The network has the ability to throttle packet transmissions which is sometimes neccessary for different types of qubit / network backends.

- `(property) packet_drop_rate(float)` : The probability that a packet is dropped on transmission in the network

- `(property) x_error_rate(float)` : The probability that a qubit has an X gate applied to in at each host in the route

- `(property) z_error_rate(float)` : The probability that a qubit has an Z gate applied to in at each host in the route

- `draw_classical_network` : Generate a depiction of the classical network

- `draw_quantum_network` : Generate a depiction of the quantum network (via matplotlib)

#### Network Object
_class_ `qunetsim.components.network.Network`

More info about the object's methods : https://tqsd.github.io/QuNetSim/components/network.html

### Protocols
---
`qunetsim.components.protocols._decode_superdense`(_q1_, _q2_)
Returns the message encoded into q1 with the support of q2
**"Encode : Encoding classical bits into a quantum state"**
- q1 : the qubit the message is encoded into. **carries quantum state changes** that represent classical bits
- q2 : the supporting entangled pair. **entangled partner needed to decode those bits**
- returns : a string of decoded message

`qunetsim.components.protocols._encode_superdense`(_message_, _q_)
Encodes qubit q with the 2 bit message
- message : message to encode
- q : qubit to encode the message

`qunetsim.components.protocols._rec_classical`(_packet_)
Receives a classical message packet , parses it into sequence number and message and sends an ACK message to receiver

`qunetsim.components.protocols._rec_epr`(_packet_)
Receives an epr qubit

`qunetsim.components.protocols._rec_ghz`(_packet_)
Receives a GHZ state and stores it in quantum storage.

`qunetsim.components.protocols._rec_key`(_packet_)
Receive a QKD key

`qunetsim.components.protocols._rec_qubit`(_packet_)
Receive a packet containing qubit information (qubit is transmitted externally)

`qunetsim.components.protocols._rec_superdense`(_packet_)
Receives a superdense qubit and decodes it.

`qunetsim.components.protocols._rec_teleport`(_packet_)
Receives a classical message (measurement result) and applies the required operations to EPR pair entangled with the sender to retrieve the teleported qubit.

`qunetsim.components.protocols._rec_w`(_packet_)
Receives a W state and stores it in quantum storage.

`qunetsim.components.protocols._relay_message`(_packet_)
Reduce TTL of network packet and if TTL > 0, sends the message to be relayed to the next node in the network and modifies the header.

`qunetsim.components.protocols._send_ack`(_sender_, _receiver_, _seq_number_)
Send an acknowledge message from the sender to the receiver. 

`qunetsim.components.protocols._send_classical`(_packet_)
Sends a classical message to another host.

`qunetsim.components.protocols._send_epr`(_packet_)
Sends an EPR to another host in the network

`qunetsim.components.protocols._send_ghz`(_packet_)
Gets GHZ qubits and distributes the to all hosts. One qubit is stored in own storage.

`qunetsim.components.protocols._send_qubit`(_packet_)
Transmit the qubit

`qunetsim.components.protocols._send_superdense`(_packet_)
Encodes and sends a qubit to send a superdense message.

`qunetsim.components.protocols._send_teleport`(_packet_)
Does the measurements for teleportation of a qubit and sends the measurement results to another host.

`qunetsim.components.protocols._send_w`(_packet_)
Gets W qubits and distributes the to all hosts. One qubit is stored in own storage.

`qunetsim.components.protocols.encode`(_sender_, _receiver_, _protocol_, _payload=None_, _payload_type=''_, _sequence_num=-1_, _await_ack=False_)
Encodes the data with the sender, receiver, protocol, payload type and sequence number and forms the packet with data and the header.

`qunetsim.components.protocols.process`(_packet_)
Decodes the packet and processes the packet according to the protocol in the packet header.

## Network Objects
### Message
Message objects are created when a Host sends a classical message. The string content of the classical message is structured as a message object with some extra content. Acknowledgements are also send as classical messages and therefore will appear in the Host's classical storage
- `property content` : content of the msg, string

- `property sender :` sender_id of the message, string

- `property seq_num` : sequence number of the message
### Qubit
Wrapper for the underlying qubit that is defined in the backend. It has a uniqueID and they know which Host they belong to

- _class_ `qunetsim.objects.qubit.Qubit`(_host_, _qubit=None_, _q_id=None_, _blocked=False_)
A qubit object. It is a wrapper class of qubits of different backends
	- H() : perform hadamard gate on the qubit
	- I() : Perform identity operation
	- K()
	- T()
	- X()
	- Y()
	- Z()
	- property blocked
	- cnot(target)
	- cphase(target)
	- `density_operator`()
	- fidelity(other_qubit) : Determines the quantum fidelity between this and the given qubit.
	- property host
	- property id
	- `measure`(_non_destructive=False_) : measure the state of a qubit
	- _property_ `qubit`
	- `release`() : release a qubit from the system
	- send_to(receiver_id) : send qubit to another host
### Quantum Storage
Are used by the Host components. Each host has 2 quantum storage objects, one for EPR pairs and the other for data qubits, but in both cases, they store Qubit objects

_class_ `qunetsim.objects.storage.quantum_storage.QuantumStorage`
- An object which stores qubit
- `_add_request`(_args_) : Adds a new request to the quantum storage. If a new qubit arrives, it is checked if the request for the qubit is satisfied
	- **args** (_list_) – [Queue, from_host_id, q_id, purpose]
	
- `_check_all_requests`() : Checks if any of the pending requests is now fulfilled

- `_check_memory_limits`(_host_id_) : Checks if another qubit can be added to the storage

- `_check_qubit_in_system`(_qubit_, _from_host_id_, _purpose=None_) : True if qubit with same parameters already in the systems

- `_decrease_qubit_counter`(_host_id_) : Checks if the qubit counter can be decreased and decreases the counter

- `_increase_qubit_counter`(_host_id_) : Checks if the qubit counter can be increased, because of memory limits, and increases the counter

- `_remove_request`(_req_id_) : Removes a pending request from the request dict

- `_reset_qubit_counter`(_host_id_)

- `add_qubit_from_host`(_qubit_, _purpose_, _from_host_id_)

- `change_qubit_id`(_from_host_id_, _new_id_, _old_id=None_)

- `check_qubit_from_host_exists`(_from_host_id_, _purpose=None_) : Check if a qubit from a host exists in this quantum storage.

- `get_all_qubits_from_host`(_from_host_id_, _purpose=None_, _remove=False_) 

- `get_qubit_by_id`(_q_id_)

- `get_qubit_from_host`(_from_host_id_, _q_id=None_, _purpose=None_, _wait=0_)

- `release_storage`()

- `reset_qubits_from_host`(_from_host_id_, _purpose=None_) : Remove all stored qubits from the host _from_host_id_.

- `reset_storage`()

- `set_storage_limit_with_host`(_new_limit_, _host_id_) : host_id is optional
### Classical Storage
It is a component of a Host used to store **message** objects
- `_add_new_host_id`(_host_id_) : Add a new host to the storage

- `_add_request`(_args_) : Adds a new request to the classical storage. If a new message arrives, it is checked if the request for the qubit is satisfied
	- args : list of [Queue, from, host_id, type,...]
	- returns ID of the request
	
- `_check_all_requests`() : Checks if any of the pending requests is now fulfilled. If a request is fulfilled, the request is handled and the function returns the message of this request

- `_remove_request`(_req_id_) : Removes a pending request from the request dict

- `add_msg_to_storage`(_message_) : Adds a message to the storage

- `empty`() : empty the classical storage

- `get_all`() : Get all messages as a list

- `get_all_from_sender`(_sender_id_, _wait=0_) : Get all stored messages from a sender. If delete option is set, the returned messages are removed from the storage

- `get_next_from_sender`(_sender_id_, _wait=0_) : Gets the next, unread, message from the sender. If there is no message yet, it is waited for the waiting time till a message is arrived. If there is still no message, than None is returned.

- `get_with_seq_num_from_sender`(_sender_id_, _seq_num_, _wait=0_) 

- `remove_all_ack`(_from_sender=None_) : Removes all ACK messages stored. If from sender is given, only ACKs from this sender are removed.
### Quantum Connection
An object that stores quantum connection details
`class qunetsim.objects.connections.quantum_connection.`QuantumConnection`(_sender_id_, _receiver_id_, model=None_)`

- property model : Channel model, an object containing model characteristics
- property receiver_id : receiver ID
- property sender_id : sender ID
### Classical Connection
Classical connection object, an object that stores classical connection details
`class qunetsim.objects.connections.classical_connection.ClassicalConnection`(_sender_id_, _receiver_id_, _model=None_)

- property model : Channel model, an object containing model characteristics
- property receiver_id : receiver ID
- property sender_id : sender ID
### Packet
Packet objects are created by the Protocol component. They are analogous to transport layer packets in the internet. They encode the sender and receiver of the packet along with the other properties. Generally, users will not need to interact with Packet objects directly

_class_ `qunetsim.objects.packets.packet.Packet`(_sender_, _receiver_, _protocol_, _payload_type_, _payload_, _sequence_number=-1_, _await_ack=False_)
- a transport layer packet
- _property_ `await_ack` : if the packet triggers an ACK request
- _property_ `payload` : payload object
- _property_ `payload_type` : classical, quantum
- _property_ `protocol` : protocol constant (Eg. Constants.SEND_TELEPORT)
- _property_ `receiver` : rec_id
- _property_ `sender` : sender_id
- _property_ `seq_num` : seq num of packet
### Routing Packet
Similar to packet object but it is analogous to a network layer packet from the internet. Difference is that these packets have a TTL property such that they are eliminated from the network after some numbers of relays or hops in the network

_class_ `qunetsim.objects.packets.routing_packet.RoutingPacket`(_sender_, _receiver_, _protocol_, _payload_type_, _payload_, _ttl_, _route_)
- `decrease_ttl`()
- _property_ `payload`
- _property_ `payload_type`
- _property_ `protocol`
- _property_ `receiver`
- _property_ `route` : the route the packet should take, returns a list of host IDs which the packet will travel
- _property_ `sender`
- _property_ `ttl` : 0 = packet is removed from the network