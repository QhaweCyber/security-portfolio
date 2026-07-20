# Home Lab: Vulnerable Service Recon on Metasploitable2

**Author:** Ntokozo Mngomeni — final-year BSc Computer Science student, University of Limpopo. Aspiring SOC analyst.

> This is a learning exercise, not a live engagement. Metasploitable2 is Rapid7's official, publicly-distributed intentionally-vulnerable training VM, run entirely inside my own isolated home lab (VirtualBox, no internet exposure). No real system or third party is involved.

## Overview

Built a small home lab (Kali Linux + Metasploitable2, both isolated on a VirtualBox NAT Network) to practice full-port service enumeration and to build the habit of recognizing well-known vulnerable service versions on sight — a core skill for a SOC analyst reviewing asset/vulnerability scan output.

## Lab setup

- **Attacker machine:** Kali Linux (VirtualBox VM)
- **Target machine:** Metasploitable2 (VirtualBox VM), official Rapid7 image
- Both VMs attached to the same isolated **NAT Network** (`10.0.0.0/24`), with no bridge to the host's real network or the internet
- Target IP for this scan: `10.0.0.5`

## Scan performed

```
nmap -sV -p- -Pn 10.0.0.5
```

- `-sV` — detect service name and version on each open port
- `-p-` — scan the full 65,535 port range, not just common ports
- `-Pn` — skip host-discovery ping (some VMs don't reliably respond to ICMP inside a NAT network, even when fully up)

## Key findings

29 open ports total. The standouts, with why each one matters:

| Port | Service | Why it's significant |
|---|---|---|
| 21 | vsftpd 2.3.4 | Famous supply-chain backdoor (CVE-2011-2523) — an attacker compromised the source distribution years ago and planted a backdoor triggered by a specific login string. One of the most-cited teaching examples in offensive security. |
| 1524 | "Metasploitable root shell" | Nmap's own service fingerprint flags this as a bind shell with **no authentication** — a deliberately planted backdoor for training. |
| 23 | Telnet | Transmits all data, including credentials, in plaintext. Considered obsolete by modern standards for exactly this reason. |
| 6667/6697 | UnrealIRCd | Another known backdoored version (CVE-2010-2075) — a classic teaching vulnerability alongside vsftpd. |
| 139/445 | Samba (SMB, 3.x-4.x) | Old SMB implementations have a long history of remote code execution CVEs; this version family is commonly used to teach SMB-based attack paths. |
| 3306 | MySQL 5.0.51a | Ancient version with known authentication-bypass and privilege-escalation issues. |
| 8180 | Apache Tomcat / Coyote | Old Tomcat installs are commonly vulnerable to default-credential and malicious-WAR-deployment attacks. |
| 512/513/514 | rexec/rlogin/rsh ("r-services") | Legacy remote-login protocols predating modern authentication standards — essentially no real access control by today's expectations. |

Full raw scan output is in [`nmap-scan-output.txt`](./nmap-scan-output.txt).

## Why this matters for defensive/SOC work

A SOC analyst rarely needs to *exploit* these — the actual job is usually **recognizing the version number in an asset inventory or vulnerability scanner report and immediately understanding the severity**, without needing to look every CVE up from scratch. Building the pattern-recognition of "vsftpd 2.3.4 = critical, patch/replace immediately" is exactly the kind of fast triage judgment this exercise was meant to build.

## Next steps for this lab

- Map each finding to its MITRE ATT&CK technique
- Practice writing the finding up as a proper vulnerability report (severity, affected asset, remediation) rather than just a raw scan list
- Extend the lab with a SIEM (Wazuh, already in my lab stack) to practice *detecting* an exploitation attempt against these services, not just finding them
