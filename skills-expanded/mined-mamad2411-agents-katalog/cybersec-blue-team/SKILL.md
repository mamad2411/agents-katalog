# Blue Team Defense & Hardening Skill

This comprehensive cybersecurity skill helps defenders implement hardening, detection engineering, and security baseline monitoring across Linux and Windows environments.

## Core Activation Triggers

The skill activates when users request assistance with:
- System hardening (Linux distros, Windows Server/workstations per CIS Benchmarks)
- Detection rule creation (Sigma, Splunk, KQL, YARA, Snort/Suricata)
- Security baseline establishment and monitoring
- Patch management strategy and prioritization
- Security architecture review (defense-in-depth, zero trust models)
- Endpoint visibility implementation (Sysmon, auditd, Windows audit policy)
- Service-specific hardening (SSH, nginx, Apache, databases)
- Post-assessment remediation planning

## Primary Capabilities

**Linux Hardening** includes SSH configuration, kernel parameter tuning via sysctl, firewall rules (UFW/iptables), file system security, and comprehensive auditd logging setup.

**Windows Hardening** provides PowerShell-based immediate controls: disabling LLMNR/NBT-NS, enabling Script Block Logging, disabling SMBv1, and Sysmon deployment with SwiftOnSecurity configurations.

**Detection Engineering** follows a five-step workflow: define behavior, collect telemetry, identify indicators, write and tune rules, then deploy and monitor. Templates are provided for Sigma, Suricata, and YARA formats.

**Security Baselines** establish normal behavior profiles for authentication, processes, networks, and file systems with automated monitoring scripts.

**Patch Management** uses a CVSS-based prioritization matrix with defined SLAs and a structured rollout process from testing through production deployment.

**Architecture Review** applies defense-in-depth layering and zero-trust assessment frameworks.

## Key Tools Referenced

- Sysmon (Windows endpoint telemetry)
- auditd (Linux audit daemon)
- Lynis (Linux security auditing)
- OpenSCAP (CIS/STIG compliance scanning)
- fail2ban (SSH brute-force protection)

The skill integrates with other security domains and references NIST, CIS Benchmarks, MITRE D3FEND, and NSA cybersecurity guidance.
