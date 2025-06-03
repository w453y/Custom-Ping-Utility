# Custom Ping Utility

This utility is a custom implementation of the ping command, written in Python. It allows you to send ICMP echo requests to a specified target (IP address or domain) and receive echo replies, providing detailed statistics about the round-trip time (RTT) and packet loss.

## Code Explanation

### `main.py`

#### Imports
- **socket**: Provides low-level networking interface.
- **argparse**: Parses command-line arguments.
- **sys**: Provides access to system-specific parameters and functions.
- **os**: Provides a way of using operating system dependent functionality.
- **math**: Provides mathematical functions.

#### Functions

- **resolve_hostname(target, force_ipv4=False, force_ipv6=False)**:
  - Resolves a hostname to an IP address.
  - Parameters:
    - `target`: The hostname or IP address to resolve.
    - `force_ipv4`: Boolean to force IPv4 resolution.
    - `force_ipv6`: Boolean to force IPv6 resolution.
  - Returns a tuple containing the resolved IP address and its version (4 or 6).

- **get_hostname(ip)**:
  - Resolves an IP address to a hostname.
  - Parameters:
    - `ip`: The IP address to resolve.
  - Returns the hostname or the IP address if the hostname cannot be resolved.

- **main()**:
  - Parses command-line arguments.
  - Ensures the script is run as root.
  - Resolves the target hostname.
  - Determines the source IP address.
  - Calls the ICMP ping function.
  - Prints detailed statistics about the ping results.

#### Code Flow
1. Parse command-line arguments using `argparse`.
2. Check if the script is run as root.
3. Resolve the target hostname to an IP address.
4. Determine the source IP address used for sending packets.
5. Call the `ping` function from `icmp_handler` to send ICMP echo requests.
6. Print detailed statistics about the ping results, including RTT and packet loss.

### `icmp_handler.py`

#### Functions

- **checksum(data)**:
  - Calculates the ICMP checksum for error detection.
  - Parameters:
    - `data`: The data to calculate the checksum for.
  - Returns the calculated checksum.

- **get_source_ip(target_ip, ip_version, interface=None)**:
  - Determines the source IP address used for outgoing packets.
  - Parameters:
    - `target_ip`: The target IP address.
    - `ip_version`: The IP version (4 or 6).
    - `interface`: The network interface to use.
  - Returns a tuple containing the source IP address and an error message (if any).

- **send_ping_request(sock, destination, sequence_number, ip_version)**:
  - Sends an ICMP Echo Request.
  - Parameters:
    - `sock`: The socket to use for sending the request.
    - `destination`: The destination IP address.
    - `sequence_number`: The sequence number of the request.
    - `ip_version`: The IP version (4 or 6).
  - Returns the time the request was sent.

- **receive_ping_reply(sock, expected_seq_number, ip_version, timeout=1)**:
  - Waits for an ICMP Echo Reply.
  - Parameters:
    - `sock`: The socket to use for receiving the reply.
    - `expected_seq_number`: The expected sequence number of the reply.
    - `ip_version`: The IP version (4 or 6).
    - `timeout`: The timeout for receiving the reply.
  - Returns a tuple containing the time the reply was received and the responder's IP address.

- **ping(target, num_requests, ip_version, interface=None, ttl=64)**:
  - Sends multiple ICMP pings and prints results immediately.
  - Parameters:
    - `target`: The target IP address.
    - `num_requests`: The number of ping requests to send.
    - `ip_version`: The IP version (4 or 6).
    - `interface`: The network interface to use.
    - `ttl`: The Time-To-Live value for the packets.
  - Returns a tuple containing an error message (if any), a list of RTT values, the number of transmitted packets, and the number of received packets.

#### Code Flow
1. Create a raw socket for sending ICMP packets.
2. Set the TTL value for the socket.
3. If a network interface is specified, bind the socket to the interface.
4. For each ping request:
   - Send an ICMP Echo Request.
   - Wait for an ICMP Echo Reply.
   - Calculate the RTT and print the result.
5. Print detailed statistics about the ping results, including RTT and packet loss.

### `test.sh`

- A shell script to run various tests on the custom ping utility.
- Tests include:
  - Pinging valid and invalid IP addresses.
  - Pinging valid and invalid domains.
  - Using different network interfaces.
  - Using different TTL values.
  - Sending different numbers of ping packets.
  - Forcing IPv4 or IPv6 resolution.

## Usage Examples

Run the script with the following command-line arguments:

```sh
sudo python3 src/main.py <target> [options]
```

## Available Arguments

```sh
usage: main.py [-h] [-c C] [-4] [-6] [-i INTERFACE] [-t TTL] target

Custom Ping Utility

positional arguments:
  target        Target IP or domain

options:
  -h, --help    show this help message and exit
  -c C          Number of ping requests (default: 5)
  -4            Force IPv4
  -6            Force IPv6
  -i INTERFACE  Specify network interface
  -t TTL        Set TTL (default: 64)
```

### Examples

1. **Ping a valid IPv4 address**:
    ```sh
    sudo python3 src/main.py 8.8.8.8 -c 3
    ```

2. **Ping a valid IPv6 address**:
    ```sh
    sudo python3 src/main.py 2001:4860:4860::8888 -c 3 -6
    ```

3. **Ping a domain**:
    ```sh
    sudo python3 src/main.py google.com -c 3
    ```

4. **Force IPv4 resolution**:
    ```sh
    sudo python3 src/main.py google.com -4 -c 3
    ```

5. **Specify a network interface**:
    ```sh
    sudo python3 src/main.py 8.8.8.8 -i wlan0 -c 3
    ```

6. **Set TTL value**:
    ```sh
    sudo python3 src/main.py 8.8.8.8 -t 10 -c 3
    ```

## Running Tests

To run the test script, use the following command:

```sh
sudo ./scripts/test.sh
```

This script will execute a series of tests to verify the functionality of the custom ping utility.

Output of the test.sh script:

```sh
========== Running Tests ==========

[TEST] Pinging a valid IPv4 address (Google DNS)
PING 8.8.8.8 (8.8.8.8) from 10.50.38.184 using default interface:
64 bytes from dns.google (8.8.8.8): icmp_seq=1 ttl=64 time=35.47 ms
64 bytes from dns.google (8.8.8.8): icmp_seq=2 ttl=64 time=39.79 ms
64 bytes from dns.google (8.8.8.8): icmp_seq=3 ttl=64 time=35.20 ms

--- Ping Statistics ---
Packets: Sent = 3, Received = 3, Lost = 0 (0.00% loss)
Minimum RTT: 35.20 ms
Maximum RTT: 39.79 ms
Average RTT: 36.82 ms
Standard Deviation RTT: 2.10 ms

[TEST] Pinging a valid IPv6 address (Google IPv6 DNS)
PING 2001:4860:4860::8888 (2001:4860:4860::8888) from 2400:4f20:11:a00::103:1e13 using default interface:
64 bytes from dns.google (2001:4860:4860::8888): icmp_seq=1 ttl=64 time=20.68 ms
64 bytes from dns.google (2001:4860:4860::8888): icmp_seq=2 ttl=64 time=20.39 ms
64 bytes from dns.google (2001:4860:4860::8888): icmp_seq=3 ttl=64 time=18.06 ms

--- Ping Statistics ---
Packets: Sent = 3, Received = 3, Lost = 0 (0.00% loss)
Minimum RTT: 18.06 ms
Maximum RTT: 20.68 ms
Average RTT: 19.71 ms
Standard Deviation RTT: 1.17 ms

[TEST] Pinging a valid domain (google.com)
PING google.com (2404:6800:4007:820::200e) from 2400:4f20:11:a00::103:1e13 using default interface:
64 bytes from maa05s25-in-x0e.1e100.net (2404:6800:4007:820::200e): icmp_seq=1 ttl=64 time=19.34 ms
64 bytes from maa05s25-in-x0e.1e100.net (2404:6800:4007:820::200e): icmp_seq=2 ttl=64 time=19.90 ms
64 bytes from maa05s25-in-x0e.1e100.net (2404:6800:4007:820::200e): icmp_seq=3 ttl=64 time=21.67 ms

--- Ping Statistics ---
Packets: Sent = 3, Received = 3, Lost = 0 (0.00% loss)
Minimum RTT: 19.34 ms
Maximum RTT: 21.67 ms
Average RTT: 20.30 ms
Standard Deviation RTT: 0.99 ms

[TEST] Pinging an invalid domain (should fail)
Error: Unable to resolve nonexistent.domain.xyz

[TEST] Pinging an invalid IP address (should fail)
Error: Unable to resolve 256.256.256.256

[TEST] Pinging localhost (IPv4)
PING 127.0.0.1 (127.0.0.1) from 127.0.0.1 using default interface:
64 bytes from localhost (127.0.0.1): icmp_seq=1 ttl=64 time=0.02 ms
64 bytes from localhost (127.0.0.1): icmp_seq=2 ttl=64 time=0.09 ms
64 bytes from localhost (127.0.0.1): icmp_seq=3 ttl=64 time=0.06 ms

--- Ping Statistics ---
Packets: Sent = 3, Received = 3, Lost = 0 (0.00% loss)
Minimum RTT: 0.02 ms
Maximum RTT: 0.09 ms
Average RTT: 0.06 ms
Standard Deviation RTT: 0.03 ms

[TEST] Pinging localhost (IPv6)
PING ::1 (::1) from ::1 using default interface:
64 bytes from localhost (::1): icmp_seq=1 ttl=64 time=0.09 ms
64 bytes from localhost (::1): icmp_seq=2 ttl=64 time=0.08 ms
64 bytes from localhost (::1): icmp_seq=3 ttl=64 time=0.07 ms

--- Ping Statistics ---
Packets: Sent = 3, Received = 3, Lost = 0 (0.00% loss)
Minimum RTT: 0.07 ms
Maximum RTT: 0.09 ms
Average RTT: 0.08 ms
Standard Deviation RTT: 0.01 ms

[TEST] Using a non-existent interface (should fail)
Error: The specified network interface 'nonexist0' does not exist or is not available.

[TEST] Using a valid interface (replace wlan0 if needed)
PING 8.8.8.8 (8.8.8.8) from 10.50.38.184 using interface wlan0:
64 bytes from dns.google (8.8.8.8): icmp_seq=1 ttl=64 time=35.46 ms
64 bytes from dns.google (8.8.8.8): icmp_seq=2 ttl=64 time=36.06 ms
64 bytes from dns.google (8.8.8.8): icmp_seq=3 ttl=64 time=35.82 ms

--- Ping Statistics ---
Packets: Sent = 3, Received = 3, Lost = 0 (0.00% loss)
Minimum RTT: 35.46 ms
Maximum RTT: 36.06 ms
Average RTT: 35.78 ms
Standard Deviation RTT: 0.25 ms

[TEST] Using different TTL values (TTL=10)
PING 8.8.8.8 (8.8.8.8) from 10.50.38.184 using default interface:
64 bytes from dns.google (8.8.8.8): icmp_seq=1 ttl=10 time=35.73 ms
64 bytes from dns.google (8.8.8.8): icmp_seq=2 ttl=10 time=35.43 ms
64 bytes from dns.google (8.8.8.8): icmp_seq=3 ttl=10 time=35.70 ms

--- Ping Statistics ---
Packets: Sent = 3, Received = 3, Lost = 0 (0.00% loss)
Minimum RTT: 35.43 ms
Maximum RTT: 35.73 ms
Average RTT: 35.62 ms
Standard Deviation RTT: 0.14 ms

[TEST] Using different TTL values (TTL=255)
PING 8.8.8.8 (8.8.8.8) from 10.50.38.184 using default interface:
64 bytes from dns.google (8.8.8.8): icmp_seq=1 ttl=255 time=36.84 ms
64 bytes from dns.google (8.8.8.8): icmp_seq=2 ttl=255 time=35.75 ms
64 bytes from dns.google (8.8.8.8): icmp_seq=3 ttl=255 time=37.29 ms

--- Ping Statistics ---
Packets: Sent = 3, Received = 3, Lost = 0 (0.00% loss)
Minimum RTT: 35.75 ms
Maximum RTT: 37.29 ms
Average RTT: 36.63 ms
Standard Deviation RTT: 0.65 ms

[TEST] Sending 1 ping packet
PING 8.8.8.8 (8.8.8.8) from 10.50.38.184 using default interface:
64 bytes from dns.google (8.8.8.8): icmp_seq=1 ttl=64 time=33.62 ms

--- Ping Statistics ---
Packets: Sent = 1, Received = 1, Lost = 0 (0.00% loss)
Minimum RTT: 33.62 ms
Maximum RTT: 33.62 ms
Average RTT: 33.62 ms
Standard Deviation RTT: 0.00 ms

[TEST] Sending 5 ping packets
PING 8.8.8.8 (8.8.8.8) from 10.50.38.184 using default interface:
64 bytes from dns.google (8.8.8.8): icmp_seq=1 ttl=64 time=52.29 ms
64 bytes from dns.google (8.8.8.8): icmp_seq=2 ttl=64 time=34.17 ms
64 bytes from dns.google (8.8.8.8): icmp_seq=3 ttl=64 time=36.26 ms
64 bytes from dns.google (8.8.8.8): icmp_seq=4 ttl=64 time=35.59 ms
64 bytes from dns.google (8.8.8.8): icmp_seq=5 ttl=64 time=54.42 ms

--- Ping Statistics ---
Packets: Sent = 5, Received = 5, Lost = 0 (0.00% loss)
Minimum RTT: 34.17 ms
Maximum RTT: 54.42 ms
Average RTT: 42.55 ms
Standard Deviation RTT: 8.88 ms

[TEST] Forcing IPv4 resolution on google.com
PING google.com (142.250.193.142) from 10.50.38.184 using default interface:
64 bytes from maa05s25-in-f14.1e100.net (142.250.193.142): icmp_seq=1 ttl=64 time=28.05 ms
64 bytes from maa05s25-in-f14.1e100.net (142.250.193.142): icmp_seq=2 ttl=64 time=31.74 ms
64 bytes from maa05s25-in-f14.1e100.net (142.250.193.142): icmp_seq=3 ttl=64 time=27.52 ms

--- Ping Statistics ---
Packets: Sent = 3, Received = 3, Lost = 0 (0.00% loss)
Minimum RTT: 27.52 ms
Maximum RTT: 31.74 ms
Average RTT: 29.10 ms
Standard Deviation RTT: 1.88 ms

[TEST] Forcing IPv6 resolution on google.com
PING google.com (2404:6800:4007:820::200e) from 2400:4f20:11:a00::103:1e13 using default interface:
64 bytes from maa05s25-in-x0e.1e100.net (2404:6800:4007:820::200e): icmp_seq=1 ttl=64 time=19.49 ms
64 bytes from maa05s25-in-x0e.1e100.net (2404:6800:4007:820::200e): icmp_seq=2 ttl=64 time=23.99 ms
64 bytes from maa05s25-in-x0e.1e100.net (2404:6800:4007:820::200e): icmp_seq=3 ttl=64 time=19.25 ms

--- Ping Statistics ---
Packets: Sent = 3, Received = 3, Lost = 0 (0.00% loss)
Minimum RTT: 19.25 ms
Maximum RTT: 23.99 ms
Average RTT: 20.91 ms
Standard Deviation RTT: 2.18 ms
========== All Tests Completed ==========
```
## Required Dependencies

- Python 3.x
- `argparse` (standard library)
- `socket` (standard library)
- `sys` (standard library)
- `os` (standard library)
- `math` (standard library)

## Supported Versions

- Python 3.6 and above


