import socket
import struct
import time
import os

def checksum(data):
    """Calculate the ICMP checksum for error detection."""
    if len(data) % 2 == 1:
        data += b'\x00'

    words = struct.unpack("!%dH" % (len(data) // 2), data)
    total = sum(words)
    total = (total >> 16) + (total & 0xFFFF)
    total += total >> 16

    return (~total) & 0xFFFF  # Return the bitwise NOT of total

def get_source_ip(target_ip, ip_version, interface=None):
    """Determine the source IP address used for outgoing packets."""
    try:
        sock_type = socket.AF_INET if ip_version == 4 else socket.AF_INET6
        sock = socket.socket(sock_type, socket.SOCK_DGRAM)

        if interface:
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, interface.encode())
            except OSError as e:
                sock.close()
                return None, f"Error: The specified network interface '{interface}' does not exist or is not available."

        sock.connect((target_ip, 1))
        source_ip = sock.getsockname()[0]
        sock.close()
        return source_ip, None  # No error

    except OSError as e:
        return None, f"Error: {e}"

def send_ping_request(sock, destination, sequence_number, ip_version):
    """Send an ICMP Echo Request."""
    icmp_type = 8 if ip_version == 4 else 128  # ICMPv4 and ICMPv6 Echo Request
    icmp_code = 0
    icmp_checksum = 0
    icmp_identifier = os.getpid() & 0xFFFF
    icmp_seq_number = sequence_number

    payload = struct.pack("!d", time.time())  # Timestamp payload
    icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_identifier, icmp_seq_number)

    if ip_version == 4:
        icmp_checksum = checksum(icmp_header + payload)
        icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_identifier, icmp_seq_number)

    packet = icmp_header + payload
    sock.sendto(packet, (destination, 0))
    return time.time()

def receive_ping_reply(sock, expected_seq_number, ip_version, timeout=1):
    """Wait for an ICMP Echo Reply."""
    sock.settimeout(timeout)
    try:
        while True:
            response, addr = sock.recvfrom(1024)
            icmp_header = response[20:28] if ip_version == 4 else response[:8]

            icmp_type, _, _, _, seq_number = struct.unpack("!BBHHH", icmp_header)

            if (ip_version == 4 and icmp_type == 0) or (ip_version == 6 and icmp_type == 129):
                if seq_number == expected_seq_number:
                    return time.time(), addr[0]
    except socket.timeout:
        return None, None

def ping(target, num_requests, ip_version, interface=None, ttl=64):
    """Send multiple ICMP pings and print results immediately."""
    transmitted = 0
    received = 0
    rtt_list = []
    
    try:
        sock = socket.socket(socket.AF_INET if ip_version == 4 else socket.AF_INET6, socket.SOCK_RAW,
                             socket.IPPROTO_ICMP if ip_version == 4 else socket.IPPROTO_ICMPV6)
        sock.setsockopt(socket.IPPROTO_IP if ip_version == 4 else socket.IPPROTO_IPV6,
                        socket.IP_TTL if ip_version == 4 else socket.IPV6_UNICAST_HOPS, ttl)

        if interface:
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, interface.encode())
            except OSError:
                return f"Warning: source address might be selected on device other than {interface}", [], 0, 0

        for i in range(1, num_requests + 1):
            transmitted += 1
            send_time = send_ping_request(sock, target, i, ip_version)
            response_time, responder_ip = receive_ping_reply(sock, i, ip_version)

            if response_time is not None:
                received += 1
                rtt = (response_time - send_time) * 1000
                
                # Resolve hostname
                try:
                    hostname = socket.gethostbyaddr(responder_ip)[0]  # Get the hostname
                except (socket.herror, socket.gaierror):
                    hostname = responder_ip  # Use IP if hostname resolution fails

                print(f"64 bytes from {hostname} ({responder_ip}): icmp_seq={i} ttl={ttl} time={rtt:.2f} ms")
                rtt_list.append((i, responder_ip, rtt))
            else:
                print(f"Request timed out for seq={i}")
                rtt_list.append((i, None, None))

            time.sleep(1)  # Mimic real ping behavior with delay

    except Exception as e:
        return f"Error: {e}", [], transmitted, received

    finally:
        sock.close()

    return None, rtt_list, transmitted, received
