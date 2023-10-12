# Custom Ping Utility

This Python script is a comprehensive custom implementation of the "ping" utility, designed to provide a deep understanding of its inner workings. It allows you to send ICMP Echo Request packets to a target IP address or domain and receive ICMP Echo Reply packets from the target. The utility calculates and displays round-trip time (RTT) for each request-reply cycle and provides extensive statistics on packet loss, minimum RTT, maximum RTT, average RTT, and RTT standard deviation.

## Explanation

### ICMP Packet Generation

At the core of this utility is the generation of ICMP (Internet Control Message Protocol) packets. ICMP is a fundamental protocol in computer networking, primarily used for error reporting and network troubleshooting. For this utility, ICMP packets serve the purpose of network diagnostics and latency measurement.

1. **Checksum Calculation**: The foundation of ICMP packet generation is the calculation of the packet's checksum. The checksum is a crucial component that ensures data integrity. It acts as a mathematical value computed over the packet's contents, enabling the detection of errors or corruption during transmission. The `checksum(data)` function plays a central role in this process.

2. **Sending ICMP Echo Requests**: The core functionality of this utility starts with the `send_ping_request(destination, sequence_number)` function. This function is responsible for creating and dispatching ICMP Echo Request packets to the target. ICMP Echo Requests are the standard "ping" messages that check the availability and responsiveness of a network host. The function operates as follows:
   - **Opening a Raw Socket**: It initiates by opening a raw socket. Raw sockets provide the capability to interact with network packets directly, allowing the construction and transmission of custom packets.
   - **Constructing the ICMP Packet**: The function constructs an ICMP Echo Request packet with several critical attributes, including:
     - **Type**: Set to 8, indicating that this is an ICMP Echo Request.
     - **Code**: Set to 0, which is the standard code for Echo Requests.
     - **Checksum**: Initially set to 0; it is computed later using the `checksum` function.
     - **Identifier**: A fixed identifier (12345) is included for tracking requests.
     - **Sequence Number**: A unique sequence number is assigned to each request, facilitating the tracking of individual requests.
   - **Sending the ICMP Packet**: With the ICMP Echo Request packet prepared, the function sends the packet to the specified destination IP address.
   - **Recording Send Time**: Importantly, the function records the time at which the request was sent. This timestamp is a critical component for measuring the round-trip time (RTT) accurately.

3. **Receiving ICMP Echo Replies**: The utility is not complete without the ability to receive ICMP Echo Reply packets. This is where the `receive_ping_reply(icmp_socket, expected_seq_number)` function comes into play. It is responsible for continuously listening for incoming ICMP packets and processing them. The function works as follows:
   - **Listening for Incoming Packets**: The function is in a continuous listening state, waiting for incoming network packets. Specifically, it's attentive to ICMP Echo Reply packets.
   - **Extracting ICMP Header**: When an ICMP packet is received, the function extracts the ICMP header from the received packet. The ICMP header contains essential information such as the type of ICMP message, code, checksum, and sequence number.
   - **Validating the Packet**: The function checks whether the received packet corresponds to an ICMP Echo Reply. For this, it looks at the ICMP message type, where type 0 signifies an ICMP Echo Reply. Furthermore, it verifies that the sequence number of the received packet matches the expected sequence number. If these conditions are met, the function proceeds with further processing.
   - **Calculating Response Time**: When the received packet is confirmed as an ICMP Echo Reply and its sequence number matches the expected sequence number, the function returns the current time as the response time. This timestamp signifies when the response was received and is critical for calculating the RTT accurately.

### Ping Functionality

The core functionality of the custom ping utility is encapsulated within the `ping` function. This function orchestrates the entire process of sending ICMP Echo Requests, receiving ICMP Echo Replies, and measuring RTT. Here is an in-depth look at how it operates:

1. **Iterating Through Requests**: The `ping` function begins by iterating through the specified number of ping requests. The number of requests is defined by the user, providing control over the number of times the ICMP Echo Request will be dispatched to the target.

2. **Sending ICMP Echo Requests**: For each iteration, the function calls the `send_ping_request` function. This initiates the process of sending an ICMP Echo Request packet to the target. As the function iterates through requests, each request generates a new ICMP Echo Request packet and dispatches it to the target.

3. **Receiving ICMP Echo Replies**: Following the dispatch of each ICMP Echo Request, the `receive_ping_reply` function is invoked. It is responsible for receiving the corresponding ICMP Echo Reply. The function enters a waiting state, eagerly awaiting the arrival of the ICMP Echo Reply that matches the ICMP Echo Request it sent.

4. **RTT Calculation**: After receiving an ICMP Echo Reply, the function calculates the Round-Trip Time (RTT). RTT is a fundamental metric in networking and provides insights into the responsiveness of a network or host. The RTT is calculated by subtracting the time at which the ICMP Echo Request was sent from the time at which the corresponding ICMP Echo Reply was received.

5. **RTT Measurement and Recording**: Each calculated RTT is recorded and stored in a list, referred to as the `rtt_list`. This list serves as a repository for all the RTT values recorded during the ping operation. By storing the RTT values in a list, the utility enables further analysis and displays extensive statistics about the network's performance and latency.

### Usage

To utilize the custom ping utility, you must execute the script using Python 3. The utility's behavior and configurations can be tailored to specific requirements by utilizing a command structure that includes various command-line arguments:

```bash
python3 ping.py <target> <num_requests>
```
![Output_Example](./png.png?raw=true "Output Example")
