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
import random
import socket
import struct
import sys
from dns_tools import DNS  # Custom module


def encode_qname(domain_name):
    """
    Encode domain name to DNS label format.
    
    Example: 'www.google.com' becomes b'\x03www\x06google\x03com\x00'
    Each label is prefixed with its length byte, and the name ends with a null byte.
    """
    labels = domain_name.split('.')
    encoded = b''
    
    for label in labels:
        # Pack the length of the label as a single byte, followed by the label bytes
        encoded += struct.pack('B', len(label)) + label.encode()
    
    # Append null byte to terminate the domain name
    encoded += b'\x00'
    return encoded


def build_dns_query(qname, qtype):
    """
    Build a complete DNS query packet.
    
    Returns the raw DNS query bytes ready to send over UDP.
    """
    # Map query type string to DNS type integer
    qtype_map = {"A": 1, "AAAA": 28}
    qtype_int = qtype_map[qtype]
    
    # DNS Header (12 bytes)
    # Format: !HHHHHH (all unsigned shorts in network byte order)
    # ID: Random 16-bit identifier
    # Flags: 0x0100 (Standard Query, Recursion Desired)
    # QDCOUNT: Number of questions (1)
    # ANCOUNT: Number of answer records (0)
    # NSCOUNT: Number of authority records (0)
    # ARCOUNT: Number of additional records (0)
    message_id = random.randint(0, 65535)
    flags = 0x0100  # Standard Query with Recursion Desired
    qdcount = 1     # One question
    ancount = 0     # No answers
    nscount = 0     # No authority records
    arcount = 0     # No additional records
    
    # Pack header using struct with network byte order (!)
    header = struct.pack('!HHHHHH', message_id, flags, qdcount, ancount, nscount, arcount)
    
    # DNS Question Section
    # QNAME: Encoded domain name (variable length)
    # QTYPE: 16-bit unsigned integer (1 for A, 28 for AAAA)
    # QCLASS: 16-bit unsigned integer (1 for IN - Internet)
    qname_encoded = encode_qname(qname)
    qclass = 1  # IN (Internet)
    question = qname_encoded + struct.pack('!HH', qtype_int, qclass)
    
    # Complete DNS query packet
    dns_query = header + question
    return dns_query


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
        sys.exit(1)

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Set socket timeout to 5 seconds
    sock.settimeout(5)

    # Generate DNS request message
    dns_query = build_dns_query(qname, qtype)

    # Send request message to server using sendto() for UDP
    try:
        sock.sendto(dns_query, server_address)
    except socket.error as e:
        print(f"Error sending DNS query: {e}")
        sock.close()
        sys.exit(1)

    # Receive message from server using recvfrom() for UDP
    try:
        raw_bytes, _ = sock.recvfrom(1024)
    except socket.timeout:
        print("Error: DNS server did not respond (timeout)")
        sock.close()
        sys.exit(1)
    except socket.error as e:
        print(f"Error receiving DNS response: {e}")
        sock.close()
        sys.exit(1)

    # Close socket
    sock.close()

    # Decode DNS message and display to screen
    DNS.decode_dns(raw_bytes)


if __name__ == "__main__":
    sys.exit(main())
