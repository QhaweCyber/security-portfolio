# Security Learning Portfolio — Ntokozo Mngomeni

Final-year BSc Computer Science student, University of Limpopo. Aspiring SOC analyst, building hands-on skills through a home lab and small real-world practice engagements.

> **A note on how this was built:** these write-ups were drafted with AI assistance for structure and clarity, but every finding, command, and result comes from hands-on testing I performed myself in my own lab and on an authorized target. I can walk through and explain every technical detail in here.

## Projects

### 1. [Informal Web Security Assessment](./scones-assessment/)
A small, authorized recon and header/config review of a friend's live e-commerce storefront (Vercel/Next.js). Covers HTTP security headers, directory enumeration (including a false-positive lesson from Vercel's bot mitigation), and scoping an authentication test correctly when the target turned out to have no login system.

**Tools used:** `curl`, `gobuster`, SecLists, browser DevTools

### 2. [Home Lab: Metasploitable2 Recon](./metasploitable2-lab/)
Full-port service enumeration against Rapid7's official vulnerable training VM, run in an isolated VirtualBox home lab. Focuses on recognizing well-known vulnerable service versions (vsftpd backdoor, UnrealIRCd backdoor, legacy r-services) — the kind of fast triage judgment a SOC analyst needs when reviewing scan output.

**Tools used:** `nmap`, VirtualBox, Kali Linux

## Home lab stack (ongoing)

VirtualBox-based lab running Kali Linux and a Windows 10 VM on an isolated NAT Network, with Sysmon, Wazuh, Wireshark, Procmon, Autoruns, Process Hacker, and Regshot for deeper monitoring/analysis practice. Currently working through a structured cybersecurity lab course and building familiarity with MITRE ATT&CK-mapped techniques.

## Contact

- LinkedIn: [ntokozo-mngomeni](https://linkedin.com/in/ntokozo-mngomeni-38b6412b3)
- GitHub: [QhaweCyber](https://github.com/QhaweCyber)
