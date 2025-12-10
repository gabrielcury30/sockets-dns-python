"""

!/usr/bin/env python3

Python DNS query client

Example usage:
  ./dns.py --type=A --name=www.ufba.br --server=8.8.8.8
  ./dns.py --type=AAAA --name=www.google.com --server=8.8.8.8

Should provide equivalent results to:
  dig www.ufba.br A @8.8.8.8 +noedns
  dig www.google.com AAAA @8.8.8.8 +noedns
  (note that the +noedns option is used to disable the pseudo-OPT
   header that dig adds. Our Python DNS client does not need
   to produce that optional, more modern header)
   
"""

import argparse
import socket
import sys
from dns_tools import DNS  # Custom module


def main():
    # Setup configuration
    parser = argparse.ArgumentParser(description='DNS client for ECPE 170')
    parser.add_argument('--type', required=True, dest='qtype',
                        help='Query Type (A or AAAA)')
    parser.add_argument('--name', required=True, dest='qname',
                        help='Query Name')
    parser.add_argument('--server', required=True, dest='server_ip',
                        help='DNS Server IP')

    args = parser.parse_args()
    qtype = args.qtype
    qname = args.qname
    server_ip = args.server_ip
    port = 53
    server_address = (server_ip, port)

    if qtype not in {"A", "AAAA"}:
        print("Error: Query Type must be 'A' (IPv4) or 'AAAA' (IPv6)")
        sys.exit()

    # Create UDP socket
    # ---------
    # STUDENT TO-DO
    # ---------

    # Generate DNS request message
    # ---------
    # STUDENT TO-DO
    # ---------

    # Send request message to server
    # (Tip: Use sendto() function for UDP)
    # ---------
    # STUDENT TO-DO
    # ---------

    # Receive message from server
    # (Tip: use recvfrom() function for UDP)
    # ---------
    # STUDENT TO-DO
    # ---------

    # Close socket
    # ---------
    # STUDENT TO-DO
    # ---------

    # Decode DNS message and display to screen
    dns.decode_dns(raw_bytes)


if __name__ == "__main__":
    sys.exit(main())
