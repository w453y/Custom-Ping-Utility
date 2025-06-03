import socket
import argparse
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import icmp_handler  # Import the ICMP handler module

def resolve_hostname(target, force_ipv4=False, force_ipv6=False):
    """Resolve hostname to an IP address based on user preference (IPv4/IPv6), avoiding unintended localhost resolution."""
    try:
        if target in ["127.0.0.1", "::1"]:  # Allow direct localhost input
            return target, 4 if target == "127.0.0.1" else 6

        if force_ipv6:
            addresses = socket.getaddrinfo(target, None, socket.AF_INET6)
            for addr in addresses:
                ip_address = addr[4][0]
                if ip_address == "::1":  # Avoid unintended localhost resolution
                    continue
                if ip_address.startswith("::ffff:"):  # Ignore IPv4-mapped IPv6 addresses
                    continue
                return ip_address, 6

        if force_ipv4:
            resolved_ip = socket.getaddrinfo(target, None, socket.AF_INET)[0][4][0]
            if resolved_ip != "127.0.0.1":  # Avoid unintended localhost resolution
                return resolved_ip, 4

        # Prefer IPv6 but fall back to IPv4 if necessary
        try:
            addresses = socket.getaddrinfo(target, None, socket.AF_INET6)
            for addr in addresses:
                ip_address = addr[4][0]
                if ip_address == "::1":  # Avoid unintended localhost resolution
                    continue
                if ip_address.startswith("::ffff:"):  # Ignore IPv4-mapped IPv6 addresses
                    continue
                return ip_address, 6
        except socket.gaierror:
            pass  # Ignore IPv6 failure, try IPv4

        try:
            resolved_ip = socket.getaddrinfo(target, None, socket.AF_INET)[0][4][0]
            if resolved_ip != "127.0.0.1":  # Avoid unintended localhost resolution
                return resolved_ip, 4
        except socket.gaierror:
            pass  # IPv4 failed too

    except socket.gaierror:
        pass  # Handle edge cases

    print(f"Error: Unable to resolve {target}")
    return None, None  # Ensure return value is always a tuple

def get_hostname(ip):
    """Resolve IP to hostname."""
    if ip is None:
        return "Unknown"
    try:
        host, _, _ = socket.gethostbyaddr(ip)
        return host
    except socket.herror:
        return ip  # Return IP if hostname can't be resolved

def main():
    """Parse arguments and execute the appropriate ping function."""
    parser = argparse.ArgumentParser(description="Custom Ping Utility")
    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("-c", type=int, default=5, help="Number of ping requests (default: 5)")
    parser.add_argument("-4", dest="force_ipv4", action="store_true", help="Force IPv4")
    parser.add_argument("-6", dest="force_ipv6", action="store_true", help="Force IPv6")
    parser.add_argument("-i", dest="interface", type=str, help="Specify network interface")
    parser.add_argument("-t", dest="ttl", type=int, default=64, help="Set TTL (default: 64)")

    args = parser.parse_args()

    if os.geteuid() != 0:
        print("Error: This script must be run as root (use sudo).")
        sys.exit(1)

    # Resolve hostname correctly
    target_ip, ip_version = resolve_hostname(args.target, args.force_ipv4, args.force_ipv6)
    if target_ip is None or ip_version is None:
        sys.exit(1)  # Exit gracefully if hostname resolution fails



    # Get the source IP used for sending packets
    source_ip, interface_error = icmp_handler.get_source_ip(target_ip, ip_version, args.interface)

    if interface_error:
        print(interface_error)
        sys.exit(1)  # Exit if we cannot bind to the specified interface

    # Handle cases where source IP is None
    if source_ip is None:
        source_ip = "Unknown"

    interface_display = f"using interface {args.interface}" if args.interface else "using default interface"

    print(f"PING {args.target} ({target_ip}) from {source_ip} {interface_display}:")

    # Call the ICMP ping function
    error_msg, rtt_list, transmitted, received = icmp_handler.ping(target_ip, args.c, ip_version, args.interface, args.ttl)

    # Print error messages if any
    if error_msg:
        print(error_msg)

    # Print detailed statistics
    print("\n--- Ping Statistics ---")
    packet_loss = ((transmitted - received) / transmitted) * 100 if transmitted else 100
    print(f"Packets: Sent = {transmitted}, Received = {received}, Lost = {transmitted - received} ({packet_loss:.2f}% loss)")
    
    if received > 0:
        rtt_values = [rtt for _, _, rtt in rtt_list if rtt is not None]
        
        min_rtt = min(rtt_values)
        max_rtt = max(rtt_values)
        avg_rtt = sum(rtt_values) / received
        
        variance = sum((rtt - avg_rtt) ** 2 for rtt in rtt_values) / received
        stddev_rtt = math.sqrt(variance)

        print(f"Minimum RTT: {min_rtt:.2f} ms")
        print(f"Maximum RTT: {max_rtt:.2f} ms")
        print(f"Average RTT: {avg_rtt:.2f} ms")
        print(f"Standard Deviation RTT: {stddev_rtt:.2f} ms")

if __name__ == "__main__":
    main()
