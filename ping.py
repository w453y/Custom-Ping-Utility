import socket
import struct
import time
import sys
import argparse
import statistics

def checksum(data):
    # Calculate the checksum for the ICMP packet
    if len(data) % 2 == 1:
        data += b'\x00'
    words = struct.unpack("!%dH" % (len(data) // 2), data)
    total = sum(words)
    total = (total >> 16) + (total & 0xFFFF)
    total += total >> 16
    return (~total) & 0xFFFF

def send_ping_request(destination, sequence_number):
    # Create a raw socket
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    # Define ICMP header
    icmp_type = 8  # ICMP Echo Request
    icmp_code = 0
    icmp_checksum = 0
    icmp_identifier = 12345
    icmp_seq_number = sequence_number

    # Create the ICMP packet
    icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_identifier, icmp_seq_number)
    icmp_checksum = checksum(icmp_header)
    icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_identifier, icmp_seq_number)

    # Send the ICMP packet
    icmp_socket.sendto(icmp_header, (destination, 0))

    # Record the time the request was sent
    send_time = time.time()

    return icmp_socket, send_time

def receive_ping_reply(icmp_socket, expected_seq_number):
    while True:
        response, _ = icmp_socket.recvfrom(1024)
        icmp_header = response[20:28]
        icmp_type, _, _, _, seq_number = struct.unpack("!BBHHH", icmp_header)
        if icmp_type == 0 and seq_number == expected_seq_number:
            return time.time()

def ping(target, num_requests):
    rtt_list = []

    for i in range(num_requests):
        icmp_socket, send_time = send_ping_request(target, i)
        response_time = receive_ping_reply(icmp_socket, i)
        icmp_socket.close()

        if response_time is not None:
            rtt = (response_time - send_time) * 1000  # in milliseconds
            rtt_list.append(rtt)
            print(f"ICMP Reply received in {rtt:.2f} ms")
        else:
            print("Request timed out")

    return rtt_list

def main():
    parser = argparse.ArgumentParser(description="Custom Ping Utility")
    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("num_requests", type=int, help="Number of ping requests")

    args = parser.parse_args()

    rtt_list = ping(args.target, args.num_requests)

    if rtt_list:
        packet_loss = (args.num_requests - len(rtt_list)) / args.num_requests * 100
        min_rtt = min(rtt_list)
        max_rtt = max(rtt_list)
        avg_rtt = statistics.mean(rtt_list)
        stdev_rtt = statistics.stdev(rtt_list)
        print(f"Packet Loss: {packet_loss:.2f}%")
        print(f"Minimum RTT: {min_rtt:.2f} ms")
        print(f"Maximum RTT: {max_rtt:.2f} ms")
        print(f"Average RTT: {avg_rtt:.2f} ms")
        print(f"RTT Standard Deviation: {stdev_rtt:.2f} ms")

if __name__ == "__main__":
    main()
