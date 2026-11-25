---
name: openclawforge-ai-security-guardian
description: >
  Use when managing VPS security, configuring firewall rules, setting up SSL certificates,
  applying security patches, or investigating security incidents on the OpenClaw platform.
---

# Security Guardian - OpenClaw AI Security Management

## Overview
Manages all security aspects of the Hostinger VPS (`srv1628373.hstgr.cloud`, IPv4: `148.230.114.25`, SSH port 65002) including firewall configuration, SSH access control, SSL/TLS certificate management, security patching, and intrusion detection for the OpenClaw platform.

## When to Use
- When configuring or updating UFW/iptables firewall rules on `srv1628373.hstgr.cloud`
- When managing SSH keys and access controls (port 65002, key-based auth enforcement)
- When installing or renewing SSL/TLS certificates for services on the VPS
- When applying security patches and updates via apt on the Ubuntu VPS
- When investigating security incidents or unusual activity on `srv1628373.hstgr.cloud`

## VPS Context
- **Hostname**: `srv1628373.hstgr.cloud`
- **IPv4**: `148.230.114.25`
- **IPv6**: `2a02:4780:28:cb4f::1`
- **SSH Port**: 65002 (non-standard, already hardened)
- See `infrastructure/vps-infrastructure.md` for detailed knowledge