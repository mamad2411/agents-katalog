<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ezrarc
description: CTF writeups and security challenges by EzraRC.
---

# Writeups by EzraRC

Source repository: `/repos/EzraRC`

## Repository Index

- Metasploitable2-Lab/README.md

## Writeup Content


### File: Metasploitable2-Lab/README.md

## Penetration Testing Report – Summary

This repository documents a **black-box penetration test** conducted against **ACME Corporation** by **myself (fake company called Target-Locked Corporation)** between **18–27 April 2023**.
The assessment simulated a real-world external attack to evaluate network security posture and identify exploitable vulnerabilities.

### Scope & Methodology

* **Testing type:** Black-box penetration test
* **Targets:**

  * Mail Server – `192.168.224.131`
  * Linux Host – `192.168.224.132`
* **Tools used:** `fping`, `nmap`, `enum4linux`, `Nessus`, `Metasploit`, `netcat`, `SSH`, `VNC`
* **Environment:** Kali Linux attack VM

### Key Findings

* The **mail server** showed **low overall risk**, with issues mainly related to:

  * Cleartext SMTP authentication
  * Weak / self-signed SSL certificates
* The **Linux host** was **critically insecure**, exposing:

  * All ports open and unfiltered
  * Weak password policies
  * Extensive information leakage via enumeration
  * Multiple critical remote access vulnerabilities

### Critical Vulnerabilities Identified

* **Bind Shell Backdoor (CVSS 9.8)**

  * Allowed unauthenticated root access via netcat
* **VNC with Default Credentials (CVSS 10.0)**

  * Enabled full remote desktop access
* **Weak SSH Algorithms**

  * Allowed SSH access using deprecated host key algorithms
  * Successful brute-force and default credential attacks

### Exploitation Results

* Achieved **root and administrative access** on the vulnerable system
* Successfully:

  * Established bind shells
  * Logged in via VNC and SSH
  * Brute-forced credentials (`msfadmin:msfadmin`)
  * Exfiltrated sensitive files using SCP
* Demonstrated a **full compromise and data breach scenario**

### Risk Assessment

* One system posed an **immediate and severe threat** to organisational security
* Attackers could:

  * Gain persistent remote access
  * Execute arbitrary commands
  * Steal or manipulate sensitive data
* Overall risk rating:

  * Mail Server: **Low**
  * Linux Host: **Critical**

### Recommendations

* Enforce **strong password policies**

  * No default credentials
  * Increased complexity
  * Regular password rotation
* **Harden port configurations**

  * Close or filter unnecessary ports
  * Apply firewall restrictions
* Apply **regular updates and patches**

  * Remove outdated and insecure services
* Disable insecure services (e.g. VNC, bind shells) unless explicitly required

### Conclusion

This assessment highlights how **misconfigurations and weak security controls** can lead to full system compromise.
The test demonstrates the importance of **regular penetration testing**, secure defaults, and proactive vulnerability management in defending enterprise networks.

