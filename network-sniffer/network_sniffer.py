#!/usr/bin/env python3
"""
Basic Network Sniffer
Author: Ntokozo Mngomeni
Captures live packets on a chosen interface and displays key info:
source/destination IP, protocol, and ports (for TCP/UDP).

For educational use only, on networks I own or have explicit permission to monitor.
"""

from scapy.all import sniff, IP, TCP, UDP, Raw

def process_packet(packet):
    # Only process packets that actually have an IP layer
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        proto = packet[IP].proto  # numeric protocol code

        # Map common protocol numbers to names
        proto_name = {6: "TCP", 17: "UDP", 1: "ICMP"}.get(proto, str(proto))

        line = f"[{proto_name}] {src_ip} -> {dst_ip}"

        # If it's TCP or UDP, we can also grab port numbers
        if TCP in packet:
            line += f" | Src Port: {packet[TCP].sport} -> Dst Port: {packet[TCP].dport}"
        elif UDP in packet:
            line += f" | Src Port: {packet[UDP].sport} -> Dst Port: {packet[UDP].dport}"

        print(line)

        # If there's a payload, show a small preview (careful: this can include plaintext creds on unencrypted protocols like HTTP/Telnet/FTP)
        if Raw in packet:
            payload = packet[Raw].load
            print(f"    Payload preview: {payload[:50]}")

if __name__ == "__main__":
    print("Starting sniffer on eth0. Press Ctrl+C to stop.\n")
    sniff(iface="eth0", filter="tcp port 23", prn=process_packet, store=False)

