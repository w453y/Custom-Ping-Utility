#!/bin/bash

# Test script for Custom Ping Utility
# Ensure the script is run with sudo
if [[ $EUID -ne 0 ]]; then
    echo "Please run this script as root (sudo ./scripts/test.sh)"
    exit 1
fi

SCRIPT="./src/main.py"  # Path to the main script

echo "========== Running Tests =========="

# 1. Test valid IPv4 ping
echo -e "\n[TEST] Pinging a valid IPv4 address (Google DNS)"
python3 $SCRIPT 8.8.8.8 -c 3

# 2. Test valid IPv6 ping
echo -e "\n[TEST] Pinging a valid IPv6 address (Google IPv6 DNS)"
python3 $SCRIPT 2001:4860:4860::8888 -c 3 -6

# 3. Test resolving a valid domain
echo -e "\n[TEST] Pinging a valid domain (google.com)"
python3 $SCRIPT google.com -c 3

# 4. Test resolving an invalid domain
echo -e "\n[TEST] Pinging an invalid domain (should fail)"
python3 $SCRIPT nonexistent.domain.xyz -c 3

# 5. Test invalid IP address
echo -e "\n[TEST] Pinging an invalid IP address (should fail)"
python3 $SCRIPT 256.256.256.256 -c 3

# 6. Test pinging localhost (IPv4)
echo -e "\n[TEST] Pinging localhost (IPv4)"
python3 $SCRIPT 127.0.0.1 -c 3

# 7. Test pinging localhost (IPv6)
echo -e "\n[TEST] Pinging localhost (IPv6)"
python3 $SCRIPT ::1 -c 3 -6

# 8. Test invalid interface (should fail)
echo -e "\n[TEST] Using a non-existent interface (should fail)"
python3 $SCRIPT 8.8.8.8 -i nonexist0 -c 3

# 9. Test valid interface (change wlan0 if necessary)
echo -e "\n[TEST] Using a valid interface (replace wlan0 if needed)"
python3 $SCRIPT 8.8.8.8 -i wlan0 -c 3

# 10. Test different TTL values
echo -e "\n[TEST] Using different TTL values (TTL=10)"
python3 $SCRIPT 8.8.8.8 -t 10 -c 3

echo -e "\n[TEST] Using different TTL values (TTL=255)"
python3 $SCRIPT 8.8.8.8 -t 255 -c 3

# 11. Test sending different packet counts
echo -e "\n[TEST] Sending 1 ping packet"
python3 $SCRIPT 8.8.8.8 -c 1

echo -e "\n[TEST] Sending 5 ping packets"
python3 $SCRIPT 8.8.8.8 -c 5

# 12. Test forcing IPv4 on a dual-stack domain
echo -e "\n[TEST] Forcing IPv4 resolution on google.com"
python3 $SCRIPT google.com -4 -c 3

# 13. Test forcing IPv6 on a dual-stack domain
echo -e "\n[TEST] Forcing IPv6 resolution on google.com"
python3 $SCRIPT google.com -6 -c 3

echo "========== All Tests Completed =========="
