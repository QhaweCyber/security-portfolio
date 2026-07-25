# Security Learning Portfolio — Ntokozo Mngomeni

Final-year BSc Computer Science student at the University of Limpopo. I'm working toward becoming a SOC analyst, so this repo is where I keep the hands-on stuff I do outside of class — home lab work, and a couple of small real-world practice assessments.

I'm still learning. Some of this is basic compared to what an experienced analyst would do, but everything here is stuff I actually ran and worked through myself.

## What's in here

### 1. [Web assessment on a friend's site](./scones-assessment/)
A small e-commerce site a fellow student built (Next.js, hosted on Vercel). He let me poke around and check the security headers, try some directory enumeration, and see if there was a login system to test. Ran into an interesting false-positive along the way that taught me more than the actual findings did.

Tools: `curl`, `gobuster`, SecLists, browser dev tools

### 2. [Metasploitable2 home lab](./metasploitable2-lab/)
Full port scan against Rapid7's official vulnerable practice VM, running in an isolated VirtualBox network on my own machine. Mostly about training myself to recognize dangerous service versions on sight instead of having to look every single one up.

Tools: `nmap`, VirtualBox, Kali Linux

## My home lab (ongoing)

Running VirtualBox with Kali Linux and a Windows 10 VM on an isolated NAT network. I've got Sysmon, Wazuh, Wireshark, Procmon, Autoruns, Process Hacker, and Regshot set up for monitoring and analysis practice. Currently working through a structured cybersecurity lab course and getting familiar with MITRE ATT&CK.

## Contact

- LinkedIn: [ntokozo-mngomeni](https://linkedin.com/in/ntokozo-mngomeni-38b6412b3)
- GitHub: [QhaweCyber](https://github.com/QhaweCyber)
