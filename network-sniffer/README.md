# Basic Network Sniffer

I built a Python packet sniffer using scapy and used it to capture and analyze live traffic on my home lab network. Point of the exercise was to actually see why plaintext protocols are dangerous, not just be told about it.

## What it does

Captures packets on a chosen interface and prints out the source IP, destination IP, protocol, and ports. If there's a payload, it shows a preview of it too.

## Setup

- Kali Linux VM, Python 3.11.6, scapy 2.7.0
- Same isolated NAT network (10.0.0.0/24) as my Metasploitable2 lab
- Ran the sniffer filtered to `tcp port 23` while connecting to my Metasploitable2 VM's Telnet service (msfadmin/msfadmin)

## What I found

Telnet sends everything, including login credentials, completely unencrypted. In the capture, you can watch the username and password come through one letter at a time, since Telnet sends each keystroke as its own packet with no buffering at all.

Full raw capture is in [`telnet-capture-output.txt`](./telnet-capture-output.txt) — you can literally read `m`, `s`, `f`, `a`, `d`, `m`, `i`, `n` appear one at a time right after the login prompt, and the same thing happens again for the password.

## Why this matters for SOC work

This is the exact reason Telnet is considered obsolete and SSH replaced it. Anyone with visibility into network traffic — a compromised switch, a rogue access point, an attacker who's already on the network — can grab credentials just by watching, no exploitation needed. Recognizing plaintext protocols like Telnet, FTP, and unencrypted HTTP in a network is a basic but important part of spotting risk.

## Files in this folder

- `network_sniffer.py` — the sniffer script
- `telnet-capture-output.txt` — captured evidence of the plaintext login
