# Home Lab: Vulnerable Service Recon on Metasploitable2

**Author:** Ntokozo Mngomeni — final-year BSc Computer Science student, University of Limpopo. Aspiring SOC analyst.

Quick note before anything else: Metasploitable2 is Rapid7's official, publicly released training VM — it's *meant* to be scanned and broken. This isn't a real target, and I ran the whole thing inside my own isolated home lab with no internet exposure.

## What I did

I set up Kali Linux and Metasploitable2 as two VirtualBox VMs on the same isolated NAT network (`10.0.0.0/24`), then ran a full port scan against the target to see everything that was open, not just the common ports. The point wasn't really to hack anything — it was to build the habit of looking at a service name and version and immediately knowing "that's bad" without having to Google every single one.

## The scan

```
nmap -sV -p- -Pn 10.0.0.5
```

- `-sV` grabs the service name/version on each port
- `-p-` scans all 65,535 ports instead of just the common ones
- `-Pn` skips the host-alive ping check — some VMs on a NAT network don't reliably answer ICMP even when they're fully up, so this avoids a false "host down" result

Target was `10.0.0.5`, and it came back with 29 open ports. Full raw output is in [`nmap-scan-output.txt`](./nmap-scan-output.txt).

## What stood out

A few of these I already half-recognized, others I had to look up — either way, here's what I found and why it matters:

- **Port 21 — vsftpd 2.3.4.** This one's famous. Years ago someone compromised the actual source distribution of this FTP server and planted a backdoor that triggers on a specific login string. It's one of the most commonly cited examples in offensive security training for exactly that reason.
- **Port 1524 — flagged by nmap as "Metasploitable root shell."** This is a deliberately planted bind shell with no authentication at all, built into the training VM on purpose.
- **Port 23 — Telnet.** Sends everything, including passwords, in plain text. There's basically no reason to run this today.
- **Ports 6667/6697 — UnrealIRCd.** Another version with a known backdoor (CVE-2010-2075), usually taught right alongside the vsftpd one.
- **Ports 139/445 — Samba (SMB, 3.x-4.x).** Old SMB versions have a long track record of remote code execution bugs, so this is commonly used to teach SMB attack paths.
- **Port 3306 — MySQL 5.0.51a.** Very old, with known authentication bypass and privilege escalation issues.
- **Port 8180 — Apache Tomcat.** Old Tomcat setups are often vulnerable to default credentials or malicious WAR file deployment.
- **Ports 512/513/514 — rexec/rlogin/rsh.** Legacy remote login protocols from before modern authentication existed — basically no real access control by today's standards.

## Why I think this matters for SOC work

I don't think the day-to-day job is usually about exploiting these — it's about seeing "vsftpd 2.3.4" or "Telnet open" in an asset scan or vulnerability report and immediately knowing how bad that is, without needing to research it in the moment. That's really what I was trying to build here — fast triage judgment, not exploitation skill.

## What I want to do next with this lab

- Map each of these findings to a MITRE ATT&CK technique
- Practice writing these up properly as vulnerability reports (severity, affected asset, what to actually do about it) instead of just a scan list
- Hook up Wazuh (already part of my lab) and try to detect an actual exploitation attempt against these services, not just find them
